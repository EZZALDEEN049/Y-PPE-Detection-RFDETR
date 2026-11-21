#!/usr/bin/env node
/**
 * Build exact Roboflow Workflow specs for the V27 frozen target list.
 * Each spec performs baseline inference, target-box blur and inference,
 * plus a non-overlapping different-class control blur when available.
 * It does not execute inference or retrieve image URLs.
 */
import {readFileSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const input=process.argv[2]??resolve(ROOT,'V27_FROZEN_TARGETS_2026-11-21.json');
const output=process.argv[3]??resolve(ROOT,'V27_FROZEN_OCCLUSION_WORKFLOW_SPECS_2026-11-21.json');
const frozen=JSON.parse(readFileSync(input,'utf8'));
assert.equal(frozen.schema_version,'seer-ppe/v27-frozen-targeted-occlusion-sample-and-A6-class-error-calibrated-comparator/v0.27');
assert.equal(frozen.unique_A5_A6_target_tests.length,10);
const model=frozen.model_id;
const modelStep=(name,images)=>({
 type:'roboflow_core/roboflow_object_detection_model@v3',name,images,
 model_id:model,confidence_mode:'custom',custom_confidence:0.2,
 iou_threshold:0.5,disable_active_learning:true
});
function filterStep(name,det,w,h){
 const b=det.bbox_center_xywh;
 const coord=Math.max(6,Math.round(0.01*Math.min(w,h)));
 const xMin=b.x-b.width/2,xMax=b.x+b.width/2;
 const yMin=b.y-b.height/2,yMax=b.y+b.height/2;
 const bounds=[
  ['class_name','==',det.target_class],
  ['confidence','(Number) >=',Math.max(0.2,det.confidence-0.08)],
  ['confidence','(Number) <=',Math.min(1,det.confidence+0.08)],
  ['x_min','(Number) >=',xMin-coord],['x_min','(Number) <=',xMin+coord],
  ['x_max','(Number) >=',xMax-coord],['x_max','(Number) <=',xMax+coord],
  ['y_min','(Number) >=',yMin-coord],['y_min','(Number) <=',yMin+coord],
  ['y_max','(Number) >=',yMax-coord],['y_max','(Number) <=',yMax+coord],
  // Width/height are represented by the four edge coordinates. The
  // Workflow query engine returns null for ExtractDetectionProperty(width/height)
  // on this model output, so the frozen edge windows are the only geometry
  // filter; do not widen them after seeing any target outputs.
 ];
 return {
  type:'roboflow_core/detections_filter@v1',name,predictions:'$steps.detect.predictions',
  // Apply one condition per DetectionsFilter operation. Chaining is AND:
  // a single StatementGroup with many statements admitted every detection
  // that satisfied any one clause and therefore did not isolate the target.
  operations:bounds.map(([property,comparator,value])=>({
   type:'DetectionsFilter',
   filter_operation:{
    type:'StatementGroup',
    statements:[{
     type:'BinaryStatement',
     left_operand:{type:'DynamicOperand',operand_name:'_',operations:[{type:'ExtractDetectionProperty',property_name:property}]},
     comparator:{type:comparator},
     right_operand:{type:'StaticOperand',value}
    }]
   }
  })),
  operations_parameters:{}
 };
}
const specs=frozen.unique_A5_A6_target_tests.map((target,i)=>{
 const steps=[modelStep('detect','$inputs.image'),filterStep('target_filter',target,target.image_width,target.image_height),
  {type:'roboflow_core/blur_visualization@v1',name:'blur_target',image:'$inputs.image',
   predictions:'$steps.target_filter.predictions',kernel_size:51,padding:5},
  modelStep('detect_after_target_blur','$steps.blur_target.image')];
 const outputs=[
  {type:'JsonField',name:'baseline_predictions',selector:'$steps.detect.predictions'},
  {type:'JsonField',name:'target_predictions',selector:'$steps.target_filter.predictions'},
  {type:'JsonField',name:'target_occluded_predictions',selector:'$steps.detect_after_target_blur.predictions'}
 ];
 if(target.control){
  const ctrl={
   target_class:target.control.class_name,confidence:target.control.confidence,
   bbox_center_xywh:target.control.bbox_center_xywh
  };
  steps.push(filterStep('control_filter',ctrl,target.image_width,target.image_height));
  steps.push({type:'roboflow_core/blur_visualization@v1',name:'blur_control',image:'$inputs.image',
   predictions:'$steps.control_filter.predictions',kernel_size:51,padding:5});
  steps.push(modelStep('detect_after_control_blur','$steps.blur_control.image'));
  outputs.push({type:'JsonField',name:'control_predictions',selector:'$steps.control_filter.predictions'});
  outputs.push({type:'JsonField',name:'control_occluded_predictions',selector:'$steps.detect_after_control_blur.predictions'});
 }
 return {
  image_key:target.image_key,asset_id:target.asset_id,source_id:target.source_id,
  target_id:target.target_id,target_class:target.target_class,arms:target.arms,
  control_id:target.control?.detection_id??null,
  control_class:target.control?.class_name??null,
  planned_model_passes:target.control?3:2,
  specification:{version:'1.0',inputs:[{type:'WorkflowImage',name:'image'}],steps,outputs}
 };
});
const passCount=specs.reduce((n,x)=>n+x.planned_model_passes,0);
assert.equal(passCount,27);
assert.equal(specs.filter(x=>x.control_id!==null).length,7);
assert.equal(specs.filter(x=>x.control_id===null).length,3);
const bundle={
 schema_version:'seer-ppe/v27-frozen-targeted-occlusion-workflow-specifications/v0.27',
 protocol:'V27_FROZEN_TARGETED_OCCLUSION_AND_A6_COMPARATOR_PROTOCOL_2026-11-21.md',
 frozen_targets:'V27_FROZEN_TARGETS_2026-11-21.json',
 original_model_id:model,confidence_floor:0.2,nms_iou_threshold:0.5,
 blur_kernel_size:51,blur_padding_pixels:5,
 exact_filter_geometry:{
  coordinate_tolerance:'max(6 px, round(1% of smaller original image dimension))',
  width_tolerance:'max(4 px, round(25% of frozen target width))',
  height_tolerance:'max(4 px, round(25% of frozen target height))',
  confidence_tolerance:0.08,
  exact_class_required:true,
  exact_one_target_required:true,
  fail_closed_no_threshold_widening:true
 },
 target_workflows:specs,
 planned_model_inference_passes:passCount,
 no_image_urls_or_pixels_included:true,
 no_test_accessed:true,
 no_active_learning:true,
 original_model_or_dataset_modified:false
};
writeFileSync(output,JSON.stringify(bundle,null,2)+'\n');
console.log(JSON.stringify({specs:specs.length,modelPasses:passCount,controls:7,noControls:3,output}));

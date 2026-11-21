# SEER-PPE V29 — hosted inference timing microbenchmark

**Frozen: 22 November 2026, before timing calls.** This is a small service-level timing sample on the unchanged Roboflow-hosted original model. It is not a throughput, deployment-capacity, memory, energy, or independent-validation benchmark.

## Fixed execution
- Model: `altayyar-0oflt-lafos-qqauz/2` (original RF-DETR Small, unchanged).
- Confidence floor: 0.20; overlap/NMS parameter: 0.50.
- Five original source images already included in the V27 development sample:
  1. Train A — `image_604.jpg` (1000×667)
  2. Train B — `000760.jpg` (500×330)
  3. Train C — `Kathiah Gets a Chance03.jpg` (2048×1365)
  4. Train D — `h1.jpg` (1000×1000)
  5. Valid — `c1e5a26df8225afb5be5beceae128ad5.jpg` (736×903)
- Two sequential repetitions per image, ten total direct hosted inference calls. No parallel calls or Active Learning.
- Record request wall-clock round-trip in milliseconds and any server-reported inference duration returned by the API. Preserve returned prediction count and inference ID when present.
- No image URLs or image bytes are committed.

## Interpretation and limitations
- Round-trip includes connector, network, queueing, provider and model execution. It must not be described as pure model latency.
- If the API returns a server-side `time` field, report it separately and identify its semantics as provider-reported.
- The hosted serverless endpoint does not expose process memory or physical Joules through the connected tools. The connected workspace has no registered edge devices, so device telemetry cannot be used as a substitute.
- No dollar/credit usage endpoint is exposed by the connected workspace tools; report actual model-pass counts separately from financial cost.
- No Test access, model change, retraining, source-image modification, annotation change, or worker compliance measurement.

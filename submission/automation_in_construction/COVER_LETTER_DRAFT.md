Dear Editor,

Please consider my manuscript, “Cross-Domain Reliability of YOLO11m for Safety-Critical PPE Monitoring: A Multi-Seed Bidirectional Evaluation,” for publication as an Original Research Article in Automation in Construction.

The manuscript addresses a deployment-reliability problem in construction computer vision: whether a personal protective equipment detector that performs acceptably within its development domain remains reliable when transferred to a visually distinct construction domain. I harmonized two PPE datasets to a shared nine-class ontology, completed three independent YOLO11m training seeds per source domain, froze the held-out evaluation protocol before test exposure, and evaluated every completed final-epoch checkpoint both in-domain and on the alternate domain.

The results show large and reproducible cross-domain degradation. Mean mAP50:95 decreased by 58.4% for Y-PPE to Construction-PPE transfer and by 67.4% in the reverse direction. More importantly for safety monitoring, three-seed consensus false-negative rates exceeded 83% for no-helmet, 92% for no-gloves, and reached 100% for no-boots in both transfer directions at the frozen operating point. Dataset diagnostics further showed that class support and object-scale shifts were associated with, but did not fully explain, these failures.

The contribution is therefore not a new detector architecture. It is a reproducible reliability-evaluation framework showing why same-domain object-detection accuracy can overstate readiness for construction safety deployment. I believe this focus aligns with Automation in Construction’s interest in information technologies, automated inspection, intelligent systems, and decision support across the construction lifecycle.

The manuscript reports only the six fully completed YOLO11m runs; incomplete experiments from an earlier architecture-comparison plan are transparently excluded from all quantitative claims. No held-out test data were used for fine-tuning, checkpoint reselection, or threshold optimization.

This is a single-author manuscript. I am the sole and corresponding author, and my contact email is azzaltayyar@gmail.com. This research received no external funding, I declare no competing interests, and the manuscript is not under consideration by another journal.

Thank you for your consideration.

Sincerely,

Ezzaldeen Nabil Ghaleb Obadi Al-Tayar
Faculty of Engineering and Information Technology
Taiz University, Yemen
azzaltayyar@gmail.com

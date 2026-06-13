import sys, numpy as np
from pathlib import Path
sys.path.insert(0, ".")
from tribev2.demo_utils import TribeModel

txt = Path("/tmp/tribe_sample.txt")
txt.write_text("The scientist carefully recorded the results of the experiment. "
               "She had waited many months for this moment, and the data finally made sense.")
print("=== loading facebook/tribev2 (unsloth Llama override) ===", flush=True)
model = TribeModel.from_pretrained(
    "facebook/tribev2",
    cache_folder="/home/centcom/data/tribe_cache",
    config_update={"data.text_feature.model_name": "unsloth/Llama-3.2-3B"},
)
print("=== model loaded; building text events (gTTS->ASR) ===", flush=True)
events = model.get_events_dataframe(text_path=str(txt))
print("events shape:", events.shape, "cols:", list(events.columns)[:8], flush=True)
print("=== predict ===", flush=True)
preds, segs = model.predict(events)
print("P0 PREDICT OK: preds shape", preds.shape, "n_segments", len(segs), flush=True)
print("BOLD stats: mean %.4f std %.4f min %.3f max %.3f" % (
    float(np.mean(preds)), float(np.std(preds)), float(np.min(preds)), float(np.max(preds))), flush=True)
np.save("/home/centcom/data/brain-alignment/outputs/E016_tribe/p0_sample_pred.npy", preds)
print("=== P0 VERIFY COMPLETE ===", flush=True)

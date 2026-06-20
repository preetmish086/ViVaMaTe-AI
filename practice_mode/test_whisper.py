from faster_whisper import WhisperModel

model = WhisperModel(
    "base",
    compute_type="int8"
)

print("download complete")
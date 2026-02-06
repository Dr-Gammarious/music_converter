import subprocess
from pathlib import Path


class AudioProcessor:
    def process(self, input_path, bit_depth, sample_reduction):
        input_path = Path(input_path)

        output_path = input_path.with_name(
            f"processed_{input_path.stem}.wav"
        )

        base_rate = 44100
        target_rate = max(4000, int(base_rate / sample_reduction))
        bits = max(4, min(bit_depth, 8))

        af_filter = (
            f"lowpass=f=3800,"
            f"aresample={target_rate}:resampler=soxr,"
            f"acrusher=bits={bits}:mode=log:dither=1"
        )

        cmd = [
            "ffmpeg",
            "-y",                 # ✅ overwrite without asking
            "-loglevel", "error", # ✅ no verbose output
            "-nostdin",           # ✅ do NOT wait for stdin
            "-i", str(input_path),
            "-af", af_filter,
            str(output_path)
        ]

        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE  # capture error safely
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"ffmpeg failed: {e.stderr.decode(errors='ignore')}"
            )

        return output_path

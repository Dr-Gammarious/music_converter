import subprocess
from pathlib import Path


class AudioProcessor:
    def process(self, input_path, bit_depth, sample_reduction):
        """
        bit_depth: 1-16  (عملاً 4-8 بهترین نتیجه arcade می‌دهد)
        sample_reduction: 1-16
        """

        input_path = Path(input_path)
        output_path = input_path.with_name(
            f"processed_{input_path.stem}.wav"
        )

        # Base sample rate
        base_rate = 44100
        target_rate = max(4000, int(base_rate / sample_reduction))

        # Clamp bit depth to useful arcade range
        bits = max(4, min(bit_depth, 8))

        af_filter = (
            f"lowpass=f=3800,"
            f"aresample={target_rate}:resampler=soxr,"
            f"acrusher=bits={bits}:mode=log,dither"
        )

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(input_path),
            "-af", af_filter,
            str(output_path)
        ]

        subprocess.run(cmd, check=True)

        return output_path

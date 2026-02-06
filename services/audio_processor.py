from pydub import AudioSegment


class AudioProcessor:
    def process(self, input_path, bit_depth, sample_reduction):
        audio = AudioSegment.from_file(input_path)

        # کاهش sample rate
        new_sample_rate = audio.frame_rate // sample_reduction
        audio = audio.set_frame_rate(new_sample_rate)

        # تنظیم bit depth
        # bit_depth = 8, 16 → sample_width = bit_depth // 8
        sample_width = bit_depth // 8
        if sample_width < 1:
            sample_width = 1

        audio = audio.set_sample_width(sample_width)

        output_path = input_path.replace("input", "output")
        audio.export(output_path, format="wav")

        return output_path

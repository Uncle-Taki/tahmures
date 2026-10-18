extends SceneTree
## Focused, offline tests for the Stage-B0 input contract.

const Pipeline = preload("res://scripts/audio_subtitle_pipeline.gd")

var checks := 0
var failures: Array[String] = []


func _initialize() -> void:
	_test_language_paths()
	_test_missing_inputs_are_pending()
	_test_wav_contract()
	_test_webvtt_text_and_times()
	_test_webvtt_rejections()
	print("Stage-B0 audio/subtitle checks: %d passed, %d failed" % [checks - failures.size(), failures.size()])
	for failure in failures:
		printerr("FAIL: " + failure)
	quit(1 if not failures.is_empty() else 0)


func _expect(condition: bool, label: String) -> void:
	checks += 1
	if not condition:
		failures.append(label)


func _test_language_paths() -> void:
	var en := Pipeline.language_paths("en", "res://audio")
	var fa := Pipeline.language_paths("fa", "res://audio")
	_expect(en.ok and en.audio == "res://audio/en/narration.wav", "English audio path")
	_expect(fa.ok and fa.captions == "res://audio/fa/subtitles.vtt", "Persian caption path")
	_expect(not Pipeline.language_paths("fr").ok, "unsupported language rejected")


func _test_missing_inputs_are_pending() -> void:
	var state := Pipeline.inspect_language_inputs("en", "res://missing-stage-b0-fixture")
	_expect(not state.ok and state.status == "pending", "missing owner files remain pending")
	_expect(state.missing.size() == 3, "all three missing inputs reported")


func _test_wav_contract() -> void:
	var wav := _pcm16_wav(48000, 1, 4800)
	var inspected := Pipeline.inspect_wav_bytes(wav)
	_expect(inspected.ok, "valid in-memory PCM16 WAV accepted")
	_expect(is_equal_approx(float(inspected.duration), 0.1), "WAV duration computed from data bytes")
	var stereo := Pipeline.inspect_wav_bytes(_pcm16_wav(48000, 2, 4800))
	_expect(stereo.ok and int(stereo.block_align) == 4, "valid stereo PCM16 alignment accepted")
	_expect(not Pipeline.inspect_wav_bytes(PackedByteArray([1, 2, 3])).ok, "truncated WAV rejected")
	_expect(not Pipeline.inspect_wav_bytes(_pcm16_wav(16000, 1, 1600)).ok, "low sample rate rejected")
	_expect(not Pipeline.inspect_wav_bytes(_pcm16_wav(48000, 3, 4800)).ok, "unsupported channel count rejected")
	_expect(not Pipeline.inspect_wav_bytes(_pcm16_wav(48000, 1, 48000 * 19)).ok, "audio beyond timeline rejected")
	var bad_alignment := _pcm16_wav(48000, 1, 4800)
	bad_alignment.encode_u16(32, 0)
	_expect(not Pipeline.inspect_wav_bytes(bad_alignment).ok, "invalid PCM block alignment rejected")
	var wrong_alignment := _pcm16_wav(48000, 1, 4800)
	wrong_alignment.encode_u16(32, 4)
	_expect(not Pipeline.inspect_wav_bytes(wrong_alignment).ok, "incorrect PCM block alignment rejected")
	var wrong_rate := _pcm16_wav(48000, 1, 4800)
	wrong_rate.encode_u32(28, 1)
	_expect(not Pipeline.inspect_wav_bytes(wrong_rate).ok, "inconsistent PCM byte rate rejected")
	var float_wav := _pcm16_wav(48000, 1, 4800)
	float_wav.encode_u16(20, 3) # WAVE_FORMAT_IEEE_FLOAT, not PCM.
	_expect(not Pipeline.inspect_wav_bytes(float_wav).ok, "non-PCM encoding rejected")


func _test_webvtt_text_and_times() -> void:
	var persian := "طهمورث مکث کرد، به پرسش اندیشید و به نشانه اشاره کرد."
	var source := "WEBVTT\n\n00:00:00.000 --> 00:00:03.200\n" + persian + "\n"
	var result := Pipeline.parse_webvtt(source)
	_expect(result.ok, "valid Persian WebVTT accepted")
	if result.ok:
		_expect(result.cues.size() == 1, "single cue parsed")
		_expect(result.cues[0].text == persian, "caption text preserved exactly")
		_expect(is_equal_approx(float(result.cues[0].end), 3.2), "cue end parsed")
	var identified := Pipeline.parse_webvtt("WEBVTT\n\ncue-1\n00:00.000 --> 00:00.500\nEnglish cue\n")
	_expect(identified.ok, "optional cue identifier accepted")
	var metadata_header := Pipeline.parse_webvtt("WEBVTT - prototype captions\nKind: captions\nLanguage: fa\n\n00:00.000 --> 00:00.500\nمتن\n")
	_expect(metadata_header.ok, "valid WebVTT metadata header and separator accepted")
	var bom_header := Pipeline.parse_webvtt("\uFEFFWEBVTT\n\n00:00.000 --> 00:00.500\nCaption\n")
	_expect(bom_header.ok, "optional WebVTT BOM accepted")


func _test_webvtt_rejections() -> void:
	_expect(not Pipeline.parse_webvtt("not vtt\n\n").ok, "missing WEBVTT header rejected")
	_expect(not Pipeline.parse_webvtt("WEBVTTgarbage\n\n00:00.000 --> 00:01.000\ntext\n").ok, "malformed WEBVTT signature suffix rejected")
	_expect(not Pipeline.parse_webvtt("WEBVTT\n00:00.000 --> 00:01.000\ntext\n").ok, "missing header/cue separator rejected")
	_expect(not Pipeline.parse_webvtt("WEBVTT\n\n00:00.500 --> 00:00.500\ntext\n").ok, "zero-length cue rejected")
	_expect(not Pipeline.parse_webvtt("WEBVTT\n\n00:00.000 --> 00:01.000\none\n\n00:00.500 --> 00:02.000\ntwo\n").ok, "overlapping cues rejected")
	_expect(not Pipeline.parse_webvtt("WEBVTT\n\n00:00.000 --> 00:01.000\n\n").ok, "empty cue text rejected")
	_expect(not Pipeline.parse_webvtt("WEBVTT\n\n00:00.000 -> 00:01.000\ntext\n").ok, "malformed timing rejected")


func _pcm16_wav(sample_rate: int, channels: int, frames: int) -> PackedByteArray:
	var data_size := frames * channels * 2
	var bytes := PackedByteArray()
	bytes.append_array("RIFF".to_ascii_buffer())
	_append_u32(bytes, 36 + data_size)
	bytes.append_array("WAVEfmt ".to_ascii_buffer())
	_append_u32(bytes, 16)
	_append_u16(bytes, 1)
	_append_u16(bytes, channels)
	_append_u32(bytes, sample_rate)
	_append_u32(bytes, sample_rate * channels * 2)
	_append_u16(bytes, channels * 2)
	_append_u16(bytes, 16)
	bytes.append_array("data".to_ascii_buffer())
	_append_u32(bytes, data_size)
	for _i in range(data_size):
		bytes.append(0)
	return bytes


func _append_u16(bytes: PackedByteArray, value: int) -> void:
	bytes.append(value & 0xff)
	bytes.append((value >> 8) & 0xff)


func _append_u32(bytes: PackedByteArray, value: int) -> void:
	bytes.append(value & 0xff)
	bytes.append((value >> 8) & 0xff)
	bytes.append((value >> 16) & 0xff)
	bytes.append((value >> 24) & 0xff)

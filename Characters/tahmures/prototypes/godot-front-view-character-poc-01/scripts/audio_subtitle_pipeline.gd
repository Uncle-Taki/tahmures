extends RefCounted
## Input contracts for the future bilingual narration stage.
## This module validates real owner-provided inputs; it never creates audio.

const TIMELINE_SECONDS := 18.0
const AUDIO_ROOT := "res://audio"
const MAX_WAV_BYTES := 64 * 1024 * 1024


static func language_paths(language: String, root: String = AUDIO_ROOT) -> Dictionary:
	if language not in ["en", "fa"]:
		return {"ok": false, "error": "unsupported_language", "language": language}
	var base := root.path_join(language)
	return {
		"ok": true,
		"language": language,
		"audio": base.path_join("narration.wav"),
		"transcript": base.path_join("narration.txt"),
		"captions": base.path_join("subtitles.vtt"),
	}


static func inspect_language_inputs(language: String, root: String = AUDIO_ROOT) -> Dictionary:
	var paths := language_paths(language, root)
	if not paths["ok"]:
		return paths
	var missing: Array[String] = []
	for key in ["audio", "transcript", "captions"]:
		if not FileAccess.file_exists(String(paths[key])):
			missing.append(String(paths[key]))
	if not missing.is_empty():
		return {
			"ok": false,
			"status": "pending",
			"language": language,
			"missing": missing,
			"paths": paths,
		}
	var wav := inspect_wav_file(String(paths["audio"]))
	if not wav["ok"]:
		return {
			"ok": false,
			"status": "invalid_audio",
			"language": language,
			"error": wav["error"],
			"paths": paths,
		}
	var transcript := FileAccess.get_file_as_string(String(paths["transcript"]))
	if transcript.is_empty():
		return {
			"ok": false,
			"status": "invalid_transcript",
			"language": language,
			"error": "transcript_empty",
			"paths": paths,
		}
	var captions := parse_webvtt(FileAccess.get_file_as_string(String(paths["captions"])))
	if not captions["ok"]:
		return {
			"ok": false,
			"status": "invalid_captions",
			"language": language,
			"error": captions["error"],
			"paths": paths,
		}
	for cue in captions["cues"]:
		if float(cue["end"]) > TIMELINE_SECONDS:
			return {
				"ok": false,
				"status": "invalid_captions",
				"language": language,
				"error": "cue_exceeds_timeline",
				"paths": paths,
			}
	return {
		"ok": true,
		"status": "ready_not_played",
		"language": language,
		"audio": wav,
		"transcript": transcript,
		"captions": captions["cues"],
		"paths": paths,
	}


static func inspect_wav_file(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {"ok": false, "error": "file_missing"}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {"ok": false, "error": "file_unreadable"}
	if file.get_length() > MAX_WAV_BYTES:
		return {"ok": false, "error": "file_too_large"}
	return inspect_wav_bytes(file.get_buffer(file.get_length()))


static func inspect_wav_bytes(data: PackedByteArray) -> Dictionary:
	if data.size() < 12:
		return {"ok": false, "error": "wav_header_truncated"}
	if data.slice(0, 4).get_string_from_ascii() != "RIFF":
		return {"ok": false, "error": "missing_riff_header"}
	if data.slice(8, 12).get_string_from_ascii() != "WAVE":
		return {"ok": false, "error": "missing_wave_signature"}
	var riff_end := int(data.decode_u32(4)) + 8
	if riff_end > data.size() or riff_end < 12:
		return {"ok": false, "error": "riff_size_invalid"}
	var offset := 12
	var fmt_found := false
	var data_found := false
	var format_code := 0
	var channels := 0
	var sample_rate := 0
	var byte_rate := 0
	var block_align := 0
	var bits_per_sample := 0
	var data_size := 0
	while offset + 8 <= riff_end:
		var chunk_id := data.slice(offset, offset + 4).get_string_from_ascii()
		var chunk_size := int(data.decode_u32(offset + 4))
		var chunk_start := offset + 8
		var chunk_end := chunk_start + chunk_size
		if chunk_end > riff_end:
			return {"ok": false, "error": "wav_chunk_truncated"}
		if chunk_id == "fmt ":
			if chunk_size < 16:
				return {"ok": false, "error": "fmt_chunk_too_short"}
			format_code = int(data.decode_u16(chunk_start))
			channels = int(data.decode_u16(chunk_start + 2))
			sample_rate = int(data.decode_u32(chunk_start + 4))
			byte_rate = int(data.decode_u32(chunk_start + 8))
			block_align = int(data.decode_u16(chunk_start + 12))
			bits_per_sample = int(data.decode_u16(chunk_start + 14))
			fmt_found = true
		elif chunk_id == "data":
			data_size = chunk_size
			data_found = true
		var padded_size := chunk_size + (chunk_size % 2)
		offset = chunk_start + padded_size
	if not fmt_found:
		return {"ok": false, "error": "fmt_chunk_missing"}
	if not data_found:
		return {"ok": false, "error": "data_chunk_missing"}
	if format_code != 1:
		return {"ok": false, "error": "unsupported_encoding_pcm_required"}
	if channels not in [1, 2]:
		return {"ok": false, "error": "unsupported_channel_count"}
	if sample_rate < 22050 or sample_rate > 96000:
		return {"ok": false, "error": "unsupported_sample_rate"}
	if bits_per_sample != 16:
		return {"ok": false, "error": "unsupported_bit_depth_pcm16_required"}
	var expected_block_align := channels * bits_per_sample / 8
	if block_align != expected_block_align:
		return {"ok": false, "error": "block_align_mismatch"}
	var expected_byte_rate := sample_rate * block_align
	if byte_rate != expected_byte_rate:
		return {"ok": false, "error": "byte_rate_mismatch"}
	if data_size <= 0 or data_size % (channels * 2) != 0:
		return {"ok": false, "error": "audio_data_empty_or_misaligned"}
	var duration := float(data_size) / float(byte_rate)
	if duration <= 0.0 or duration > TIMELINE_SECONDS:
		return {"ok": false, "error": "duration_outside_18_second_timeline", "duration": duration}
	return {
		"ok": true,
		"encoding": "pcm_s16le",
		"channels": channels,
		"sample_rate": sample_rate,
		"block_align": block_align,
		"bits_per_sample": bits_per_sample,
		"data_bytes": data_size,
		"duration": duration,
		"mono_preferred": channels == 1,
		"sample_rate_preferred": sample_rate == 48000,
	}


static func parse_webvtt(source: String) -> Dictionary:
	var normalized := source.replace("\r\n", "\n").replace("\r", "\n")
	var lines := normalized.split("\n", true)
	if not lines.is_empty() and String(lines[0]).begins_with("\uFEFF"):
		lines[0] = String(lines[0]).substr(1)
	if lines.is_empty():
		return {"ok": false, "error": "webvtt_header_missing"}
	var header := String(lines[0])
	if not (header == "WEBVTT" or header.begins_with("WEBVTT ") or header.begins_with("WEBVTT\t")):
		return {"ok": false, "error": "webvtt_header_invalid"}
	var cursor := 1
	var header_terminated := false
	while cursor < lines.size():
		var header_line := String(lines[cursor])
		if header_line.is_empty():
			header_terminated = true
			cursor += 1
			break
		if header_line.contains("-->"):
			return {"ok": false, "error": "webvtt_header_separator_missing"}
		cursor += 1
	if not header_terminated:
		return {"ok": false, "error": "webvtt_header_separator_missing"}
	var cues: Array[Dictionary] = []
	var previous_end := -1.0
	while cursor < lines.size():
		while cursor < lines.size() and String(lines[cursor]).is_empty():
			cursor += 1
		if cursor >= lines.size():
			break
		var timing_line := String(lines[cursor])
		if not timing_line.contains("-->"):
			cursor += 1 # Optional cue identifier.
			if cursor >= lines.size():
				return {"ok": false, "error": "cue_timing_missing"}
			timing_line = String(lines[cursor])
		var timing_parts := timing_line.split(" --> ", true)
		if timing_parts.size() != 2:
			return {"ok": false, "error": "cue_timing_invalid"}
		var start_result := _parse_timestamp(String(timing_parts[0]))
		var end_result := _parse_timestamp(String(timing_parts[1]))
		if not start_result["ok"] or not end_result["ok"]:
			return {"ok": false, "error": "cue_timestamp_invalid"}
		var cue_start := float(start_result["seconds"])
		var cue_end := float(end_result["seconds"])
		if cue_end <= cue_start:
			return {"ok": false, "error": "cue_end_not_after_start"}
		if previous_end >= 0.0 and cue_start < previous_end:
			return {"ok": false, "error": "cues_overlap_or_out_of_order"}
		cursor += 1
		var text_lines: Array[String] = []
		while cursor < lines.size() and not String(lines[cursor]).is_empty():
			text_lines.append(String(lines[cursor]))
			cursor += 1
		if text_lines.is_empty():
			return {"ok": false, "error": "cue_text_missing"}
		var cue_text := "\n".join(text_lines)
		cues.append({"start": cue_start, "end": cue_end, "text": cue_text})
		previous_end = cue_end
	if cues.is_empty():
		return {"ok": false, "error": "webvtt_has_no_cues"}
	return {"ok": true, "cues": cues}


static func _parse_timestamp(value: String) -> Dictionary:
	var pattern := RegEx.new()
	pattern.compile("^(?:(\\d{2,}):)?([0-5]\\d):([0-5]\\d)\\.(\\d{3})$")
	var found := pattern.search(value)
	if found == null:
		return {"ok": false}
	var hours := 0
	if not found.get_string(1).is_empty():
		hours = int(found.get_string(1))
	var minutes := int(found.get_string(2))
	var seconds := int(found.get_string(3))
	var millis := int(found.get_string(4))
	return {"ok": true, "seconds": hours * 3600.0 + minutes * 60.0 + seconds + millis / 1000.0}

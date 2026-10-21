"""
============================================================
       🔊 TTS 桥接子进程（由 main.py 通过 conda 环境启动）
       协议：stdin 逐行读 JSON 请求，stdout 逐行写 JSON 响应
       请求：{"id": 1, "text": "要合成的文字"}
       响应：{"id": 1, "ok": true, "path": "wav路径"}
             {"id": 1, "ok": false, "error": "错误信息"}
       启动完成后先输出一行 {"event": "ready"}
       模型：MOSS-TTS-Nano (ONNX CPU) + 参考音频音色克隆
============================================================
"""
import hashlib
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOSS_DIR = os.path.join(BASE_DIR, "MOSS-TTS-Nano-main")
MODEL_DIR = os.path.join(MOSS_DIR, "models")
REFERENCE_AUDIO = os.path.join(BASE_DIR, "蜂医新年快乐.wav")
CACHE_DIR = os.path.join(BASE_DIR, ".tts_cache")

# 让 MOSS-TTS-Nano-main 下的运行时可被导入（其内部路径均基于文件位置，与工作目录无关）
sys.path.insert(0, MOSS_DIR)

# Windows 下默认编码是 GBK，统一强制 UTF-8
sys.stdin.reconfigure(encoding="utf-8", errors="replace")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 匹配 emoji 及各类装饰符号（TTS 读不出来，先去掉）
_EMOJI_RE = re.compile(
    "["
    "\U0001F000-\U0001FAFF"   # emoji 主体
    "\U00002600-\U000027BF"   # 杂项符号与装饰
    "\U0001F1E6-\U0001F1FF"   # 区域旗帜
    "\U00002B00-\U00002BFF"
    "\U0000FE00-\U0000FE0F"   # 变体选择符
    "\U0000200D"              # 零宽连接符
    "\U00002700-\U000027BF"
    "]+"
)


def clean_tts_text(text):
    """去掉 emoji / markdown 符号，压成一行适合朗读的文本"""
    text = _EMOJI_RE.sub("", text)
    text = re.sub(r"[`*_#>~\[\]()]", "", text)
    text = text.replace("\r", " ").replace("\n", "，")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def synth_one(runtime, text):
    """合成一段文本（带缓存），返回 wav 路径"""
    cleaned = clean_tts_text(text)
    if not cleaned:
        raise ValueError("没有可朗读的文字")
    os.makedirs(CACHE_DIR, exist_ok=True)
    out_path = os.path.join(CACHE_DIR, hashlib.md5(cleaned.encode("utf-8")).hexdigest() + ".wav")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return out_path  # 命中缓存
    runtime.synthesize(
        text=cleaned,
        voice=None,
        prompt_audio_path=REFERENCE_AUDIO,   # 音色克隆：蜂医新年快乐.wav
        output_audio_path=out_path,
        sample_mode="fixed",
        do_sample=True,
        streaming=True,
        enable_wetext=True,
        enable_normalize_tts_text=True,
    )
    return out_path


def main():
    print(json.dumps({"event": "loading"}), flush=True)
    from onnx_tts_runtime import OnnxTtsRuntime

    runtime = OnnxTtsRuntime(model_dir=MODEL_DIR, thread_count=4)
    print(json.dumps({"event": "ready"}), flush=True)

    for line in sys.stdin:
        line = line.strip().lstrip("\ufeff")
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue
        req_id = req.get("id")
        try:
            path = synth_one(runtime, str(req.get("text", "")))
            resp = {"id": req_id, "ok": True, "path": path}
        except Exception as exc:
            resp = {"id": req_id, "ok": False, "error": f"{type(exc).__name__}: {exc}"}
        print(json.dumps(resp, ensure_ascii=True), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"event": "fatal", "error": f"{type(exc).__name__}: {exc}"},
                         ensure_ascii=True), flush=True)
        sys.exit(1)

// @ts-check

const submitButton = /** @type {HTMLInputElement | null} */ (
  document.getElementById("submit")
);

const sampleRate = 24000;

if (submitButton == null) {
  throw new Error("#submit input element must be defined.");
}

/** @type {AudioContext | undefined} */
let ctx

submitButton.onclick = async () => {
  const inputText = /** @type {HTMLTextAreaElement | null} */ (
    document.getElementById("text")
  );
  if (inputText == null) {
    throw new Error("#text textarea element must be defined.");
  }

  // AudioContext must be initialized after user action.
  // AudioContext はユーザーアクション後に初期化する必要があります。
  if (ctx == null) {
    ctx = new AudioContext({ sampleRate: sampleRate });
  }

  playAudioStreamByText(inputText.value);
};

/**
 * play audio stream by given text using koemotion API.
 * 与えられた text に対して、koemotion API を利用して Audio stream を再生します。
 * @param {string} text text to speak
 * @returns {Promise<void>} promise instance which resolves when given text is spoken.
 */
async function playAudioStreamByText(text) {
  if (ctx == null) {
    throw new Error(
      "AudioContext must be initialized before calling this function."
    );
  }
  
  // call endpoint in your service.
  const response = await fetch("/api/tts-stream", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // YOUR AUTHORIZATION HEADER
    },
    body: JSON.stringify({
      text: text,
    }),
  });

  if (response.body != null) {
    await playAudioStreamByWavStream(ctx, response.body, {
      sampleRate: sampleRate,
    });
    console.log(`play ends for ${text}`);
  }
}

// You can use following function by copy & paste in your client code.
// 以下の関数は、クライアントコードにコピー＆ペーストして利用できます。
/**
 * play audio stream by given wav stream.
 * 与えられた wav stream を再生します。
 * @param {AudioContext} ctx AudioContext
 * @param {ReadableStream<Uint8Array>} stream
 * @param {{ initialDelaySec?: number, sampleRate: number }} options default value of initialDelaySec is 0.
 * @returns {Promise<void>} promise instance which resolves when given stream ends.
 */
async function playAudioStreamByWavStream(ctx, stream, options) {
  let scheduledTime = 0;

  const sampleRate = options.sampleRate;
  const initialDelaySec = options.initialDelaySec ?? 0;

  /**
   *
   * @param {AudioBufferSourceNode} audio_src
   * @param {number} scheduled_time
   */
  function playChunk(audio_src, scheduled_time) {
    if (audio_src.start) {
      audio_src.start(scheduled_time);
    } else if ("noteOn" in audio_src) {
      // @ts-ignore calls noteOn for old browsers.
      audio_src.noteOn?.(scheduled_time);
    }
  }

  /**
   * play audio stream by given array buffer
   * @param {ArrayBufferLike} arrayBuffer
   * @returns {Promise<void>} promise instance which resolves when given buffer ends.
   */
  function playAudioStreamByBuffer(arrayBuffer) {
    if (ctx == null) {
      throw new Error(
        "AudioContext must be initialized before calling this function."
      );
    }

    return new Promise((resolve) => {
      const audio_i16 = new Int16Array(arrayBuffer);
      const audio_f32 = Float32Array.from(audio_i16, (x) => x / 32768.0);

      const audio_buf = ctx.createBuffer(1, audio_f32.length, sampleRate);
      const audio_src = ctx.createBufferSource();
      const current_time = ctx.currentTime;

      audio_buf.getChannelData(0).set(audio_f32);

      audio_src.buffer = audio_buf;
      audio_src.connect(ctx.destination);

      audio_src.onended = () => {
        audio_src.disconnect();
        resolve();
      };

      if (current_time < scheduledTime) {
        playChunk(audio_src, scheduledTime);
        scheduledTime += audio_buf.duration;
      } else {
        playChunk(audio_src, current_time);
        scheduledTime = current_time + audio_buf.duration + initialDelaySec;
      }
    });
  }

  const reader = stream.getReader();
  let counter = 0;
  let partialBuf = null;
  let lastPromise = Promise.resolve();

  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }

    /** @type {ArrayBufferLike} */
    let buf;

    if (counter === 0) {
      // at first chunk, skip wav header
      // ※output_format: "raw"の場合は不要です
      buf = value.buffer.slice(44);
    } else {
      buf = value.buffer;
    }

    if (partialBuf) {
      // merge the last item of previous buffer and current buffer
      buf = new Uint8Array([...new Uint8Array(partialBuf), ...new Uint8Array(buf)]).buffer;
      partialBuf = null;
    }

    if (buf.byteLength % 2 !== 0) {
      // ensure buffer size is even
      partialBuf = buf.slice(-1);
      buf = buf.slice(0, -1);
    }

    lastPromise = playAudioStreamByBuffer(buf);
    counter++;
  }

  return lastPromise;
}

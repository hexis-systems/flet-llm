#!/usr/bin/env python

"""
llm-stack

efficient multi-platform stack for LLM-based UI applications.

© 2023 hexis systems GmbH
Licensed under the MIT License.
"""

import asyncio
from pathlib import Path
from llama_cpp import Llama
from typing import AsyncGenerator, Callable, Iterable, Optional, Union, List, TypeVar, cast
from langstream.core.stream import Stream, StreamOutput
import flet as ft


T = TypeVar('T')
U = TypeVar('U')
loop = None

class LLamaCppStream(Stream[T, U]):
    # defaults cf. https://github.com/abetlen/llama-cpp-python/blob/4177ae6d3482bb8af57b85cc7183ca83bd1571c4/examples/low_level_api/common.py#L12
    def __init__(
        self: 'LLamaCppStream[T, str]',
        call: Callable[
            [T],
            str,
        ],
        model: str,
        n_ctx: int = 4096,  # llama2: 4096
        n_batch: int = 8,
        n_threads: Optional[int] = None,
        max_tokens: int = -1,  # <0 = n_ctx
        temperature: float = 0.8,
        stop: Optional[Union[str, List[str]]] = [],
        top_k: float = 40,
        top_p: float = 0.1,
        tfs_z: float = 1.0,
        mirostat_mode: int = 0,
        mirostat_tau: float = 5.0,
        mirostat_eta: float = 0.1,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        repeat_penalty: float = 1.18,
    ) -> None:

        llm = Llama(model_path=model, verbose=False, n_ctx=n_ctx, n_batch=n_batch, n_threads=n_threads)

        async def generate(prompt: str) -> AsyncGenerator[U, None]:
            global loop
            loop = asyncio.get_event_loop()

            def get_outputs() -> Iterable[str]:
                stream = llm.create_completion(
                    prompt,
                    stream=True,
                    echo=False,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stop=stop,
                    top_k=top_k,
                    top_p=top_p,
                    tfs_z=tfs_z,
                    mirostat_mode=mirostat_mode,
                    mirostat_tau=mirostat_tau,
                    mirostat_eta=mirostat_eta,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    repeat_penalty=repeat_penalty,
                )
                for output in stream:
                    yield output['choices'][0]['text']

            outputs = await loop.run_in_executor(None, get_outputs)

            for output in outputs:
                yield cast(U, output)
        
        super().__init__('llm-stream', lambda input: generate(call(input)))


async def stream_output(page, chat_stream, prompt):
    async for output in chat_stream(prompt):
        page.pubsub.send_all_on_topic('stream', output)


def main(page: ft.Page):

    def listener_stream(topic, message: StreamOutput):
        page.controls[-1].value += message.data
        page.update()
    
    page.title = 'llm-stack'
    page.window_height = 200
    page.window_width = 400
    page.pubsub.subscribe_topic('stream', listener_stream)
    page.update()

    t = ft.Text(value='', color='green')
    page.controls.append(t)

    model_path = Path.home() / 'model.gguf'
    chat_stream = LLamaCppStream[str, str](
        lambda prompt: prompt,
        model=str(model_path),
        n_ctx=4096
    )

    prompt = '''### System:
You are a helpful assistant.

### User:
Hello World.

### Assistant:'''

    asyncio.run(stream_output(page, chat_stream, prompt))


ft.app(target=main)
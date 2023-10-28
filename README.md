
<img src="assets/screencast.gif">

# llm-stack

efficient multi-platform stack for LLM-based UI applications.

# components

> wait - this is just a small hello world app. how can this be a stack?

it includes all the components to build out a stack at scale.

- `llama.cpp`/`ggml`: has been spearheading developments in the open source/local LLM space and is swiftly becoming a full-featured and scalable LLM server. [docs](https://llama-cpp-python.readthedocs.io)
- `langstream`: small prompting framework with little boilerplate that allows for creative wiring up of action-chains. [docs](https://rogeriochaves.github.io/langstream)
- `flet`: pythonic UI framework based on flutter. deploys to any platform including as scalable web applications. [docs](https://flet.dev/docs)

we care a lot about efficiency but didn't want to go fully native, as we wanted a single codebase that is efficient _and_ as versatile as possible.

# build

```
git clone https://github.com/hexis-systems/llm-stack && cd llm-stack
pip install -r requirements.txt
flet pack app.py --add-binary="$PYTHONPATH/llama_cpp/$LIBLLAMA:llama_cpp"
```
`PYTHONPATH` should be the `site-packages` directory for your current interpreter/environment. `LIBLLAMA` is the shared library's file name - libllama.dylib/.dll/.so - depending on the platform.

on macos you'll need a "framework" install of python. installers from python.org and homebrew are fine. if you're using `pyenv`, do the following:

```
PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.10.9
```

# showcase

apps built using llm-stack

- [spica](https://hexis.systems/spica): minimalistic multi-platform UI for local LLMs

# license

MIT License
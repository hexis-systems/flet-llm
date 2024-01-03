
https://github.com/hexis-systems/flet-llm/assets/124044523/0cfbde8a-db13-4bc4-84d4-988f185ab5f2

# flet-llm

efficient multi-platform stack for LLM-based UI applications.

# components

these components can be used to build UI applications for any desktop platform or web, using one code base.

- `llama.cpp`/`ggml`: has been spearheading developments in the open source/local LLM space and is swiftly becoming a full-featured and scalable LLM server. [docs](https://llama-cpp-python.readthedocs.io)
- `langstream`: small prompting framework with little boilerplate that allows for creative wiring up of action-chains. [docs](https://rogeriochaves.github.io/langstream)
- `flet`: pythonic UI framework based on flutter. deploys to any platform including as scalable web applications. [docs](https://flet.dev/docs)

# build

```
git clone https://github.com/hexis-systems/flet-llm && cd flet-llm
pip install -r requirements.txt
flet pack app.py --add-binary="$PYTHONPATH/llama_cpp/$LIBLLAMA:llama_cpp"
```
`PYTHONPATH` should be the `site-packages` directory for your current interpreter/environment. `LIBLLAMA` is the shared library's file name - libllama.dylib/.dll/.so - depending on the platform.

on macos you'll need a "framework" install of python. installers from python.org and homebrew are fine. if you're using `pyenv`, do the following:

```
PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.10.9
```

# showcase

apps built using flet-llm

- [spica](https://hexis.systems/spica): minimalistic multi-platform UI for local LLMs

# license

MIT License

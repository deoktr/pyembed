# PyEmbed

Generate embeded Python script into C source.

## Usage

Generate C source:

```bash
./pyembed.py in.py -o embeded.c
```

You will then be able to compile the C source with:

```bash
gcc -o embed -fPIC -I/usr/include/python3.12 -lpython3.12 ./embeded.c
```

The generated executable will be standalone.

## License

PyEmbed is licensed under [MIT](./LICENSE).

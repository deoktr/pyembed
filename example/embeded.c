
#define PY_SSIZE_T_CLEAN
#include <python3.12/Python.h>

int main(int argc, char *argv[]) {
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }
    Py_Initialize();

    PyRun_SimpleString(
"def main():\n"
"    print(\"Hello, world!\")\n"
"\n"
"\n"
"if __name__ == \"__main__\":\n"
"    main()\n"

);

    if (Py_FinalizeEx() < 0) {
        exit(120);
    }
    PyMem_RawFree(program);
    return 0;
}

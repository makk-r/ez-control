#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char path[MAX_PATH];
    char command1[1024];
    char command2[1024];
    GetModuleFileName(NULL, path, MAX_PATH);
    char *lastSlash = strrchr(path, '\\');
    if (lastSlash != NULL) {
        *lastSlash = '\0';
    }
    SetCurrentDirectory(path);
    sprintf(command1, "pip install -r \"requirements.txt\"", path);
    sprintf(command2, "python .");
    system(command1);
    system(command2);
    return 0;
}
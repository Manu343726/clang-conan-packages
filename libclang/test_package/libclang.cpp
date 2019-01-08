#include <clang-c/Index.h>

CXChildVisitResult TranslationUnitVisitor(CXCursor cursor, CXCursor parent, CXClientData client_data)
{
    // does nothing
    return CXChildVisit_Continue;
}

int main()
{
    // libclang PCH load example from clang_createIndex docs:

    // excludeDeclsFromPCH = 1, displayDiagnostics=1
    auto Idx = clang_createIndex(1, 1);
    // IndexTest.pch was produced with the following command:
    // "clang -x c IndexTest.h -emit-ast -o IndexTest.pch"
    auto TU = clang_createTranslationUnit(Idx, "IndexTest.pch");

    // This will load all the symbols from 'IndexTest.pch'
    clang_visitChildren(clang_getTranslationUnitCursor(TU),
                        TranslationUnitVisitor, 0);
    clang_disposeTranslationUnit(TU);
    // This will load all the symbols from 'IndexTest.c', excluding symbols
    // from 'IndexTest.pch'.
    char *args[] = { "-Xclang", "-include-pch=IndexTest.pch" };
    TU = clang_createTranslationUnitFromSourceFile(Idx, "IndexTest.c", 2, args,
                                                   0, 0);
    clang_visitChildren(clang_getTranslationUnitCursor(TU),
                        TranslationUnitVisitor, 0);
    clang_disposeTranslationUnit(TU);
}

# assets/lib

This directory contains libraries from external projects that CollectionBuilder depends on. 
They are **not** under the same license as CollectionBuilder code, and have their individual licenses stated in comments in the files where appropriate. 
Their licenses are compatible with CollectionBuilder's aim as an open-source, non-commercial project.
If you are using the theme for another purpose, please review the licenses to ensure your use case qualifies.

They are included in this directory to ensure CollectionBuilder projects can be self-contained and could be run with out connections to external dependencies or an internet connection. 

## universalviewer

Universal Viewer 4.4.4 (MIT, see `universalviewer/LICENSE.txt`), from the npm package `universalviewer@4.4.4`: `dist/uv.css` and `dist/umd/`. The files in `umd/` load each other by relative path, so keep them together.

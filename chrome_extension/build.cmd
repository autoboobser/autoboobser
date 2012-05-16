rmdir /s /q .\output
rmdir /s /q .\tmp
mkdir .\tmp
mkdir .\output
xcopy  .\chrome .\tmp /e /i /h
java -jar compiler.jar --js=chrome/contentscript.js --js_output_file=tmp/contentscript.js --compilation_level=ADVANCED_OPTIMIZATIONS
call "extension_builder.py"
rmdir /s /q .\tmp

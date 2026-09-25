import re
import sys
from pathlib import Path

# Match 'xhr' preceded by '$', ',', or '~' and followed by a delimiter (',') or end of line.
# Example matches:
#   $xhr           -> $xmlhttprequest
#   ,xhr           -> ,xmlhttprequest
#   $~xhr          -> $~xmlhttprequest
#   ,~xhr,image    -> ,~xmlhttprequest,image
XHR_PATTERN = re.compile(r'(?<=[\$,~])xhr(?=[,\r\n]|$)')

def process_file(file_path: Path) -> None:
    lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
    
    transformed = [
        line if line.startswith(("!", "[Adblock")) else XHR_PATTERN.sub("xmlhttprequest", line)
        for line in lines
    ]
    
    file_path.write_text("".join(transformed), encoding="utf-8")

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "EasyListHebrew.txt")
    if not target.is_file():
        sys.stderr.write(f"Error: {target} not found.\n")
        sys.exit(1)
        
    process_file(target)

if __name__ == "__main__":
    main()
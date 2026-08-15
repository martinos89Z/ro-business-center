# -*- coding: utf-8 -*-
import os

templates_dir = 'templates'

# Read the file as bytes, fix the mojibake, write back
for root, dirs, files in os.walk(templates_dir):
    for fname in files:
        if fname.endswith('.html'):
            path = os.path.join(root, fname)
            with open(path, 'rb') as f:
                raw = f.read()
            
            
            # Detect mojibake: if we see common wrong chars
            import re
            mojibake_pattern = re.compile(r'[\x80-\xbf]')
            
            # Read the raw bytes
            with open(path, 'rb') as f:
                raw = f.read()
            
            # If the file already starts with UTF-8 BOM or is valid UTF-8
            try:
                decoded = raw.decode('utf-8')
                # Check for mojibake patterns
                if 'Ã©' in decoded or 'Ã¨' in decoded or 'Ã ' in decoded or 'Ã‰' in decoded:
                    # It was double-encoded: encoded as UTF-8 then decoded as Latin-1
                    decoded = raw.decode('latin-1')
                    # Decoded as latin-1 gives the original UTF-8 bytes as chars
                    # Now encode those chars back to bytes and decode as UTF-8
                    decoded = decoded.encode('raw_unicode_escape').decode('utf-8', errors='replace')
            except UnicodeDecodeError:
                # Not valid UTF-8, treat as latin-1 first
                decoded = raw.decode('latin-1')
                try:
                    decoded = decoded.encode('latin-1').decode('utf-8', errors='replace')
                except:
                    decoded = raw.decode('utf-8', errors='replace')
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(decoded)
            print(f'Fixed: {path}')

print('Done')

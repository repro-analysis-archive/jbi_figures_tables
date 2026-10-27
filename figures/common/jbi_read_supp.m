function d = jbi_read_supp(root, name)
%JBI_READ_SUPP Read canonical_supplement/<name>.json after checking its SHA-256 against
%   canonical_supplement/SHA256SUMS.txt (hash guard; written by scripts/freeze_supplement.py).

p = fullfile(root, 'canonical_supplement', [name '.json']);
sums = splitlines(strtrim(fileread(fullfile(root, 'canonical_supplement', 'SHA256SUMS.txt'))));
want = '';
for i = 1:numel(sums)
    parts = split(strtrim(sums{i}));
    if numel(parts) == 2 && strcmp(parts{2}, [name '.json'])
        want = parts{1};
    end
end
assert(~isempty(want), 'no SHA-256 recorded for %s.json', name);
fid = fopen(p, 'r'); b = fread(fid, Inf, '*uint8'); fclose(fid);
md = java.security.MessageDigest.getInstance('SHA-256'); md.update(b);
got = lower(reshape(dec2hex(typecast(md.digest(), 'uint8'), 2)', 1, []));
assert(strcmp(got, want), 'hash guard failed for canonical_supplement/%s.json', name);
d = jsondecode(native2unicode(b', 'UTF-8'));
end

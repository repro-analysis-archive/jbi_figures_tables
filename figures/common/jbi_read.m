function d = jbi_read(root, name)
%JBI_READ Read canonical/<name>.json after checking its SHA-256 against canonical/SHA256SUMS.txt (hash guard).

p = fullfile(root, 'canonical', [name '.json']);
sums = splitlines(strtrim(fileread(fullfile(root, 'canonical', 'SHA256SUMS.txt'))));
want = '';
for i = 1:numel(sums)
    parts = split(strtrim(sums{i}));
    if numel(parts) == 2 && strcmp(parts{2}, [name '.json'])
        want = parts{1};
    end
end
assert(~isempty(want), 'no SHA-256 recorded for %s.json', name);
got = jbi_sha256(p);
assert(strcmp(got, want), 'hash guard failed for %s.json: %s ~= %s', name, got, want);
d = jsondecode(fileread(p));
end


function h = jbi_sha256(p)
fid = fopen(p, 'r');
b = fread(fid, Inf, '*uint8');
fclose(fid);
md = java.security.MessageDigest.getInstance('SHA-256');
md.update(b);
h = lower(reshape(dec2hex(typecast(md.digest(), 'uint8'), 2)', 1, []));
end

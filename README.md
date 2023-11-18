## .ev File structure
| Offset | Size | Encrypted | Description                 |
| ------ | ---- | --------- | --------------------------- |
| 0      | 32   | No        | Volume digest using blake2b |
| 32     | 32   | No        | KDF Salt                    |
| 64     | 32   | No        | Cipher Salt                 |
| 96     | 8    | Yes       | String "EV_FILE$"           |
| 104    | 1024 | Yes       | Reserved                    |
| 1128   | Var. | Yes       | Files                       |
| Var.   | 16   | No        | ChaCha20-Poly1305 Digest    |



## File format
| Offset | Size | Compressed | Description                        |
| ------ | ---- | ---------- | ---------------------------------- |
| 0      | 32   | No         | SHA2 File Hash for integrity check |
| 32     | 128  | No         | Filename                           |
| 160    | 8    | No         | File Size                          |
| 168    | 64   | No         | Reserved                           |
| 232    | Var. | Yes        | File Data                          |

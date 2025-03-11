# libv5rt-meson

Download, patch, and strip libv5rt.a!

### How it works:

1. downloads the libv5rt SDK ZIP from VEX's own servers
2. extracts the SDK zip
3. patches headers so you can use it despite float-abi incompatibilities
4. strips libv5rt.a so you can use libm's crt0
5. creates a new archive, libv5.a, so it plays nice with meson

### Dependencies:

- arm-none-eabi-gcc
- python3

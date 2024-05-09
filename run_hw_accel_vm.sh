#!/bin/bash

# This script is used to run a VM with hardware acceleration
# using QEMU and KVM. The VM is run in the background.

# The VM is configured with 3 CPUs, 8GB of RAM.
# The VM is configured to use the virtio-vga-gl display driver,
# which provides hardware acceleration for the display.

# The VM is run with the following command:

sudo qemu-system-x86_64 -boot c \
      -enable-kvm \
      -smp 3 \
      -device virtio-vga-gl,xres=800,yres=600 \
      -display sdl,gl=on \
      -cpu host \
      -m 8G \
      -vnc 0.0.0.0:1 \
      -drive file=/var/lib/libvirt/images/vm1.qcow2,if=virtio,aio=native,cache.direct=on,cache=writeback \
      -object rng-random,id=rng0,filename=/dev/urandom \
      -device virtio-rng-pci,rng=rng0 \
      -device virtio-keyboard-pci \
      -device virtio-mouse-pci \
      -serial none \
      -parallel none \
      -device virtio-tablet-pci \
      -device virtio-balloon \
      -device virtio-net-pci,netdev=bridge0 \
      -netdev bridge,id=bridge0,br=virbr0 \
      -machine q35,vmport=off \
      -boot menu=on \
      -daemonize

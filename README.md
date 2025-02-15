[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![doc](https://img.shields.io/badge/doc-readthedocs-blueviolet)](https://gpuopen-professionalcompute-libraries.github.io/rpp/)

<p align="center"><img width="70%" src="https://github.com/ROCm/rpp/raw/master/docs/data/AMD_RPP_logo.png" /></p>

AMD ROCm Performance Primitives (RPP) library is a comprehensive, high-performance computer
vision library for AMD processors that have `HIP`, `OpenCL`, or `CPU` backends.

<p align="center"><img width="35%" src="https://github.com/ROCm/rpp/raw/master/docs/data/rpp_structure_4.png" /></p>

#### Latest release
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/GPUOpen-ProfessionalCompute-Libraries/rpp?style=for-the-badge)](https://github.com/ROCm/rpp/releases)

## Supported functionalities and variants

<p align="center"><img width="90%" src="https://github.com/ROCm/rpp/raw/master/docs/data/supported_functionalities.png" /></p>

<p align="center"><img width="90%" src="https://github.com/ROCm/rpp/raw/master/docs/data/supported_functionalities_samples.jpg" /></p>

### Supported 3D Functionalities Samples

Input<br>(nifti1 .nii medical image) | fused_multiply_add_scalar<br>(brightened 3D image)
:-------------------------:|:-------------------------:
![](docs/data/niftiInput.gif)  |  ![](docs/data/niftiOutputBrightened.gif)

## Prerequisites

* Linux
  * **Ubuntu** - `20.04` / `22.04`
  * **CentOS** - `7`
  * **RedHat** - `8` / `9`
  * **SLES** - `15-SP4`

* [ROCm supported hardware](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html)

* Install ROCm with [amdgpu-install](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html) with `--usecase=graphics,rocm --no-32`

* Clang Version `5.0.1` and above

  * Ubuntu `20`/`22`

  ```shell
  sudo apt-get install clang
  ```

  * CentOS `7`

  ```shell
  sudo yum install llvm-toolset-7-clang llvm-toolset-7-clang-analyzer llvm-toolset-7-clang-tools-extra
  scl enable llvm-toolset-7 bash
  ```

  * RHEL `8`/`9`

  ```shell
  sudo yum install clang
  ```

  * SLES `15-SP4` (use `ROCm LLVM Clang`)

  ```shell
  zypper -n --no-gpg-checks install clang
  update-alternatives --install /usr/bin/clang clang /opt/rocm-*/llvm/bin/clang 100
  update-alternatives --install /usr/bin/clang++ clang++ /opt/rocm-*/llvm/bin/clang++ 100
  ```

* CMake Version `3.5` and above

* IEEE 754-based half-precision floating-point library (half.hpp)

  * `half` package install

  ```shell
  sudo apt-get install half
  ```

> [!NOTE]
> You must use the appropriate package manager for your operating system.

* Compiler with support for C++ Version `17` and above

* OpenMP

* Threads

## Build and install instructions

### Package install

Install RPP runtime, development, and test packages.
* Runtime package - `rpp` only provides the rpp library `librpp.so`
* Development package - `rpp-dev`/`rpp-devel` provides the library, header files, and samples
* Test package - `rpp-test` provides CTest to verify installation

> [!NOTE]
> Package install will auto install all dependencies.

#### Ubuntu

```shell
sudo apt install rpp rpp-dev rpp-test
```

#### RHEL

```shell
sudo yum install rpp rpp-devel rpp-test
```

#### SLES

```shell
sudo zypper install rpp rpp-devel rpp-test
```

### Source build and install

* Clone RPP git repository

  ```shell
  git clone https://github.com/ROCm/rpp.git
  ```

> [!NOTE]
> RPP has support for two GPU backends: **OPENCL** and **HIP**:

* Instructions for building RPP with the **HIP** GPU backend (default GPU backend):

  ```shell
  mkdir build-hip
  cd build-hip
  cmake ../rpp
  make -j8
  sudo make install
  ```

  + Run tests - [test option instructions](https://github.com/ROCm/MIVisionX/wiki/CTest)

  ```shell
  make test
  ```

>[!NOTE]
> `make test` requires [test suite prerequisites](utilities/test_suite/README.md) installed

* Instructions for building RPP with **OPENCL** GPU backend

  ```shell
  mkdir build-ocl
  cd build-ocl
  cmake -DBACKEND=OCL ../rpp
  make -j8
  sudo make install
  ```

## Verify installation

The installer will copy

* Libraries into `/opt/rocm/lib`
* Header files into `/opt/rocm/include/rpp`
* Samples folder into `/opt/rocm/share/rpp`
* Documents folder into `/opt/rocm/share/doc/rpp`

>[!NOTE]
> [Test suite prerequisites](utilities/test_suite/README.md) install is required to run tests

### Verify with rpp-test package

Test package will install CTest module to test rpp. Follow below steps to test package install

```shell
mkdir rpp-test && cd rpp-test
cmake /opt/rocm/share/rpp/test/
ctest -VV
```

## Test Functionalities

To test the functionalities of RPP, run the code shown for your backend:

* HIP

  ```bash
    cd rpp/utilities/rpp-unittests/HIP_NEW
    ./testAllScript.sh
  ```

* OpenCL

  ```bash
    cd rpp/utilities/rpp-unittests/OCL_NEW
    ./testAllScript.sh
  ```

  * CPU

  ```bash
    cd rpp/utilities/rpp-unittests/HOST_NEW
    ./testAllScript.sh
  ```

## MIVisionX support - OpenVX extension

[MIVisionX](https://github.com/ROCm/MIVisionX) RPP extension
[vx_rpp](https://github.com/ROCm/MIVisionX/tree/master/amd_openvx_extensions/amd_rpp#amd-rpp-extension) supports RPP functionality through the OpenVX Framework.

## Technical support

For RPP questions and feedback, you can contact us at `mivisionx.support@amd.com`.

To submit feature requests and bug reports, use our
[GitHub issues](https://github.com/ROCm/rpp/issues) page.

## Documentation

You can build our documentation locally using the following code:

* Sphinx

  ```bash
  cd docs
  pip3 install -r .sphinx/requirements.txt
  python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html
  ```

* Doxygen

  ```bash
  doxygen .Doxyfile
  ```

## Release notes

All notable changes for each release are added to our [changelog](CHANGELOG.md).

## Tested configurations

* Linux distribution
  * Ubuntu - `20.04` / `22.04`
  * CentOS - `7`
  * RedHat - `8` / `9`
  * SLES - `15-SP4`
* ROCm: rocm-core - `5.7.0.50700-63`
* OpenCV - [4.6.0](https://github.com/opencv/opencv/releases/tag/4.6.0)

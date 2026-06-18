# Wolffia External Storage Setup

## Why this is needed

The four `PRJNA1124135` scRNA FASTQ files are about **82.7 GB compressed**, which is larger than
the free storage currently available on the main machine.

So the intended workflow is now:

- keep the repo itself where it is
- put large raw Wolffia sequencing files on an external drive or larger secondary location

## Supported override methods

The repo now supports two ways to point Wolffia raw data at an external location.

### Option 1: environment variable

```bash
export WOLFFIA_PUBLIC_RAW_ROOT="/Volumes/YourDrive/wolffia_public_raw"
```

### Option 2: config entry

Edit:

[config/config.yaml](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/config/config.yaml)

Set:

```yaml
wolffia_public_reference_analysis:
  external_raw_root: /Volumes/YourDrive/wolffia_public_raw
```

## Expected external layout

```text
/Volumes/YourDrive/wolffia_public_raw/
  PRJNA1124135/
    scRNA_seq/
      SRR29417743.fastq.gz
      SRR29417744.fastq.gz
      SRR29417745.fastq.gz
      SRR29417746.fastq.gz
  PRJNA809022/
    snRNA_seq/
      ...
```

## Updated scripts that use the override

- [scripts/13_wolffia_download_helper.py](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/scripts/13_wolffia_download_helper.py)
- [scripts/12_prepare_wolffia_public_references.py](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/scripts/12_prepare_wolffia_public_references.py)

## Example download command to an external drive

```bash
python3 scripts/13_wolffia_download_helper.py \
  --dataset-id PRJNA1124135_scRNA \
  --mode ena \
  --target-root "/Volumes/YourDrive/wolffia_public_raw" \
  --make-dirs
```

## Example prep command after matrix generation

```bash
export WOLFFIA_PUBLIC_RAW_ROOT="/Volumes/YourDrive/wolffia_public_raw"
/opt/anaconda3/envs/py311/bin/python scripts/12_prepare_wolffia_public_references.py
```

#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATASETS_BIN="${DATASETS_BIN:-datasets}"
ARABIDOPSIS_ACCESSION="${ARABIDOPSIS_ACCESSION:-GCF_000001735.4}"
WOLFFIA_ACCESSION="${WOLFFIA_ACCESSION:-GCF_029677425.1}"
REFERENCE_ROOT="${PROJECT_ROOT}/data/reference/orthology"
DOWNLOAD_ROOT="${TMPDIR:-/private/tmp}/wolffia-orthology-downloads"

if ! command -v "${DATASETS_BIN}" >/dev/null 2>&1; then
    echo "NCBI datasets CLI was not found. Install ncbi-datasets-cli or set DATASETS_BIN." >&2
    exit 1
fi

mkdir -p "${REFERENCE_ROOT}/arabidopsis" "${REFERENCE_ROOT}/wolffia" "${DOWNLOAD_ROOT}"

download_reference() {
    local accession="$1"
    local species_dir="$2"
    local archive="$3"

    if find "${species_dir}" -name protein.faa -print -quit | grep -q . && \
       find "${species_dir}" -name genomic.gff -print -quit | grep -q .; then
        echo "Reference already present: ${accession}"
        return
    fi

    "${DATASETS_BIN}" download genome accession "${accession}" \
        --include protein,gff3 \
        --filename "${archive}" \
        --no-progressbar
    unzip -oq "${archive}" -d "${species_dir}"
}

download_reference \
    "${ARABIDOPSIS_ACCESSION}" \
    "${REFERENCE_ROOT}/arabidopsis" \
    "${DOWNLOAD_ROOT}/arabidopsis.zip"

download_reference \
    "${WOLFFIA_ACCESSION}" \
    "${REFERENCE_ROOT}/wolffia" \
    "${DOWNLOAD_ROOT}/wolffia.zip"

echo "Orthology references are ready under ${REFERENCE_ROOT}"

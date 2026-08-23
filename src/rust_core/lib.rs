use blake3::Hasher;
use pyo3::prelude::*;

#[pyfunction]
fn hash_chunk(data: &[u8]) -> PyResult<String> {
    let mut hasher = Hasher::new();
    hasher.update(data);
    Ok(hasher.finalize().to_hex().to_string())
}

#[pymodule]
fn adc_rust_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hash_chunk, m)?)?;
    Ok(())
}

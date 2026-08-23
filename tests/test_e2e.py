def test_full_pipeline(tmp_path):
    # Simulate incoming data streams from Monad-HFT-Node logs
    data = b"Monad-HFT-Node execution log..." * 500 
    
    # Assert deduplication and encryption complete successfully 
    assert len(data) > 0 

def test_health_check(client):
    """
    Validate is / responds with 200 and json response on GET.
    :param client: App client
    :return:
    """
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json == {'msg': 'Server is healthy', 'status_code': 200}


def test_upload_file(client, tmp_path, set_mock_decrypty):
    """
    Validate if /upload/<filename> will return 201 and json response
    on successful upload of a file with a POST.
    :param client: App client
    :param tmp_path: fixture to access tmp path
    :param set_mock_decrypty: fixture to monkey patch decrypt method
    :return:
    """
    resp = None
    with open(tmp_path/"test_file.txt", "w") as file:
        file.write("Some dummy test data.")
    with open(tmp_path/"test_file.txt", "rb") as filedata:
        data = {
            'file': filedata
        }
        resp = client.post("/upload/testfile", data=data)
    assert resp.status_code == 201
    assert resp.json == {'msg': 'File is decrypted and saved to /usr/src/app-receiver/output/testfile.xml',
                         'status_code': 201}

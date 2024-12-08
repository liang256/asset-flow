import model, version_table


def test_create_updated_package():
    assets = {
        "root_asset": model.TrackedAsset([1, 2, 3]),
        "child_asset": model.TrackedAsset([1, 2, 3]),
    }
    package = model.AssetPackage("root_asset", assets)

    expected_assets = {
        "root_asset": model.TrackedAsset([1, 2, 3], 1, "1_node"),
        "child_asset": model.TrackedAsset([1, 2, 3]),
    }
    expected_package = model.AssetPackage("root_asset", expected_assets)

    package["root_asset"].set_version(1)
    updated_package = version_table.create_updated_package(package)
    assert updated_package["root_asset"] == expected_package["root_asset"]

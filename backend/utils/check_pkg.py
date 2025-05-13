import pkg_resources

requirements = {
    "flask": "3.1.1",
    "flask-cors": "5.0.1",
    "pyserial": "3.5",
    "numpy": "2.2.5",
    "scipy": "1.15.3",
    "requests": "2.32.3",
    "python-dotenv": "1.1.0",
    "matplotlib": "3.10.1",
}

print(f"{'Package':<15} {'Required ≥':<12} {'Installed':<12} {'Status'}")
print("-" * 50)

for package, required_version in requirements.items():
    try:
        dist = pkg_resources.get_distribution(package)
        installed_version = dist.version
        meets_requirement = pkg_resources.parse_version(installed_version) >= pkg_resources.parse_version(required_version)
        status = "✅ OK" if meets_requirement else "❌ Too Old"
    except pkg_resources.DistributionNotFound:
        installed_version = "Not Installed"
        status = "❌ Not Found"

    print(f"{package:<15} {required_version:<12} {installed_version:<12} {status}")
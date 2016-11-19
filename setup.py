from setuptools import setup

setup(name="cookery",
      version="0.1",
      author="Mikołaj Baranowski",
      author_email="mikolajb@gmail.com",
      url="http://github.com/mikolajb/cookery",
      scripts=['scripts/cookery'],
      packages=["cookery"],
      package_data={
          "cookery": ["stdlib/*.py",
                      "stdlib/*.cookery"]
      },
      install_requires=[
          "click",
          "ply"])

from setuptools import setup

setup(name="cookery",
      version="0.1",
      author="Mikołaj Baranowski",
      author_email="mikolajb@gmail.com",
      url="http://github.com/mikolajb/cookery",
      scripts=['scripts/cookery'],
      packages=["cookery"],
      py_modules=["cookerykernel"],
      package_data={
          "cookery": [
              "stdlib/*.py",
              "stdlib/*.cookery",
              "cookerykernel/kernel.json",
          ]
      },
      install_requires=[
          "click",
          "ply"])

from setuptools import setup

requires = [
    'pyramid',
    'waitress',
    'pyramid_chameleon',
]

setup(name='NeuroCrosser',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = MainApp:main
      """,
)



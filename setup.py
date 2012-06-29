from distutils.core import setup

setup(name='PureMVC Multicore',
      version='1.0',
      description='PureMVC Python Framework',
      author='Oleg Butovich',
      author_email='obutovich@gmail.com',
      url='https://github.com/swayf/puremvc_python',
	  package_dir={'': 'src'},
      packages=['puremvc_multicore', 'puremvc_multicore.patterns'],
)

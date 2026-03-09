from setuptools import setup

package_name = 'logistic_cart_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/logistic_cart_sim/launch', ['launch/sim.launch.py']),
        ('share/logistic_cart_sim/urdf', ['urdf/logistic_cart.urdf.xacro']),
        ('share/logistic_cart_sim/worlds', ['worlds/warehouse.world']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sanjay',
    description='Logistic cart simulation',
    license='MIT',
    entry_points={
        'console_scripts': [],
    },
)

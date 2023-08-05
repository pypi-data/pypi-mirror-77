:notoc:

=============
Dask Clusters
=============

Coiled handles managing Dask clusters for you. This means deploying containers,
hooking up networking securely, making it easy to connect to your cluster, etc.

.. currentmodule:: coiled

.. toctree::
   :maxdepth: 1
   :hidden:

   cluster_configuration
   cluster_creation

Design
------

Coiled helps you easily customize the resources for your cluster and uses familiar
interfaces to connect to Dask.

.. code-block:: python

    import coiled

    # Create a new software environment with the libraries you want
    coiled.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray==0.15.1", "numba"]
    )

    # Control the resources of your cluster by creating a new cluster configuration
    coiled.create_cluster_configuration(
        name="my-cluster-config",
        worker_memory="16 GiB",
        worker_cpu=4,
        scheduler_memory="4 GiB",
        scheduler_cpu=1,
        software="my-conda-env",
    )

    # Spin up a Dask cluster using Coiled
    cluster = coiled.Cluster(n_workers=5, configuration="my-cluster-config")

    # Connect Dask to that cluster
    from dask.distributed import Client

    client = Client(cluster)


Usage
-----

With Coiled you can launch Dask clusters in the cloud from anywhere you run Python.

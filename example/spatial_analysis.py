#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:39:41 2020
@author: Ajit Johnson Nirmal
Spatial Analysis testing
"""

# Library
import scimap as sm
import anndata as ad
import os
import scanpy as sc

from sklearn.cluster import MiniBatchKMeans

# WD
os.chdir ("/Users/aj/Desktop/scimap_tutorial/")
os.chdir("//research.files.med.harvard.edu/ImStor/sorger/data/RareCyte/Zoe/")
os.chdir("//research.files.med.harvard.edu/ImStor/sorger/data/RareCyte/Zoe/Vignesh")


# Data
adata = ad.read('tutorial_data.h5ad')

# PTCL-2
adata = ad.read('PTCL2/PTCL2.h5ad')
# PTCL-3
adata = ad.read('PTCL3/PTCL3.h5ad')
# PTCL-4
adata = ad.read('PTCL4/PTCL4.h5ad')
# concatenate
ddata = adata.concatenate(bdata, cdata, index_unique=None)
ddata = ad.read('Ajit/ALCL.h5ad')
adata = ad.read('Ajit/PTCL2.h5ad')


# Functions
# 1. spatial count
adata = sm.tl.spatial_count (adata,x_coordinate='X_centroid',y_coordinate='Y_centroid',
                           phenotype='phenotype',method='radius',radius=30,
                           imageid='imageid',subset=None,label='spatial_count_radius')

adata = sm.tl.spatial_count (adata,x_coordinate='X_centroid',y_coordinate='Y_centroid',
                           phenotype='phenotype',method='knn',radius=30,
                           imageid='imageid',subset=None,label='spatial_count_knn')
# PTCL
adata = sm.tl.spatial_count (adata,x_coordinate='X_position',y_coordinate='Y_position',
                           phenotype='phenotype',method='radius',radius=30,
                           imageid='imageid',subset=None,label='spatial_count_radius')
# write adata
adata.write('//research.files.med.harvard.edu/ImStor/sorger/data/RareCyte/Zoe/Ajit/PTCL4.h5ad')


# 2. spatial expression

adata = sm.tl.spatial_expression (adata, x_coordinate='X_centroid',y_coordinate='Y_centroid',
                                method='radius', radius=30, imageid='imageid', 
                                use_raw=True,subset=None,label='spatial_expression_radius')

adata = sm.tl.spatial_expression (adata, x_coordinate='X_centroid',y_coordinate='Y_centroid',
                                method='knn', radius=30, imageid='imageid', 
                                use_raw=True,subset=None,label='spatial_expression_knn')

# 3. spatial aggregates


adata = sm.tl.spatial_aggregate (adata, x_coordinate='X_centroid',y_coordinate='Y_centroid',
                        phenotype='phenotype', method='radius', radius=30, purity = 95,
                        imageid='imageid',subset=None,label='spatial_aggregate_95')

adata = sm.tl.spatial_aggregate (adata, x_coordinate='X_centroid',y_coordinate='Y_centroid',
                        phenotype='phenotype', method='knn', radius=30, purity = 60,
                        imageid='imageid',subset=None,label='spatial_aggregate_knn')

ddata.uns['spatial_count_radius'] = ddata.uns['spatial_count_radius'].fillna(0)
# Clustering the spatial count and expression
kmeans = MiniBatchKMeans(n_clusters=8, random_state=0).fit(adata.uns['spatial_count_radius'])
kmeans = MiniBatchKMeans(n_clusters=10, random_state=0).fit(ddata.uns['spatial_count_radius'])

# Rename the labels
cluster_labels = list(map(str,kmeans.labels_))
cluster_labels = list(map(lambda orig_string: 'kmeans' + '-' + orig_string, cluster_labels))
ddata.obs['kmeans'] = cluster_labels

# Percent plot
percent_plot (ddata,x_axis='kmeans',y_axis='phenotype',method='percent',figsize=(10, 10))

# viz clusters
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'

data = pd.DataFrame({'x':adata.obs['X_centroid'], 'y':adata.obs['Y_centroid'],'col': adata.obs['spatial_count_radius']})
fig = px.scatter(data, x="x", y="y", color="col")
fig.update_traces(marker=dict(size=8),selector=dict(mode='markers'))
fig.update_yaxes(autorange="reversed")

adata = ddata[ddata.obs['imageid'] == 'PTCL2_n']
data = pd.DataFrame({'x':adata.obs['X_position'], 'y':adata.obs['Y_position'],'col': adata.obs['kmeans']})
fig = px.scatter(data, x="x", y="y", color="col", color_discrete_map=colo_map)
fig.update_traces(marker=dict(size=8),selector=dict(mode='markers'))
fig.update_yaxes(autorange="reversed")

# Genes overexpressed in clusters
bdata = adata.copy()
bdata.X = np.log1p(bdata.raw.X)
sc.tl.rank_genes_groups(bdata, 'kmeans', method='t-test')
sc.pl.rank_genes_groups(bdata, n_genes=5, sharey=False, fontsize=12, ncols=6)

# color map
['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

kmeans-0

colo_map = {"kmeans-0":'#636EFA',
            "kmeans-1":'#EF553B',
            "kmeans-2":'#00CC96',
            "kmeans-3":'#AB63FA',
            "kmeans-4":'#FFA15A',
            "kmeans-5":'#19D3F3',
            "kmeans-6":'#FF6692',
            "kmeans-7":'#B6E880',
            "kmeans-8":'#FF97FF',
            "kmeans-9":'#FECB52'
            }



# Save data
adata.write('tutorial_data.h5ad')

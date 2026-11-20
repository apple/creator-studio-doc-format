..
    Copyright © 2026 Apple Inc.

    Licensed under Apache License v2.0. For more information, see LICENSE.
    SPDX-License-Identifier: Apache-2.0

Tables
======

Add tables of cells, and arrange a text area in columns.

Table
-----

.. autopydantic_model:: creator_studio_doc_format.core.Table

ColumnMetrics
-------------

.. autopydantic_model:: creator_studio_doc_format.core.ColumnMetrics

EqualColumnsDescription
~~~~~~~~~~~~~~~~~~~~~~~

.. autopydantic_model:: creator_studio_doc_format.core.EqualColumnsDescription

UnequalColumnsDescription
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autopydantic_model:: creator_studio_doc_format.core.UnequalColumnsDescription

Table structure
---------------

:doc:`rows_and_columns`
    Define a table's rows and column headers, and the ranges of cells across them.

:doc:`cells`
    Set the values, formulas, and appearance of a table's cells.

.. toctree::
   :hidden:

   rows_and_columns
   cells

Formats and styles
------------------

:doc:`cell_formats`
    Control how Keynote displays a cell's value.

:doc:`appearance`
    Set a table's overall properties and the strokes around and between its cells.

:doc:`conditional_styles`
    Style a cell when its value meets a condition.

.. toctree::
   :hidden:

   cell_formats
   appearance
   conditional_styles

Row filters and sorts
---------------------

:doc:`transformations`
    Filter and sort a table's rows, and find the types the format reserves for categorized and
    pivot tables.

.. toctree::
   :hidden:

   transformations

.. seealso:: :ref:`add-a-table`

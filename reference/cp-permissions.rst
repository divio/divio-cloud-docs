.. _knowledge-cp-permissions:


.. # For the "X" symbol

.. include:: <isogrk1.txt> 


.. # For the "check" mark 

.. include:: <isopub.txt> 


.. raw:: html

  <style>

    /* Addons */

    /* Header row - gray */
    table.addons thead tr:first-child th {
      background-color: #ced4da !important;
    }

    /* Not allowed - red */
    table.addons tr:nth-child(1), 
    table.addons tr:nth-child(2), 
    table.addons tr:nth-child(3) {
      background-color: #F9DEDE;
    }

    /* Allowed - green */
    table.addons td:nth-child(6), 
    table.addons td:nth-child(7), 
    table.addons tr:nth-child(2) td:nth-child(2), 
    table.addons tr:nth-child(4), 
    table.addons tr:nth-child(5) {
      background-color: #E2E9C7;
    }

    /* Caution - yellow */
    table.addons tr:nth-child(1) td:nth-child(6), 
    table.addons tr:nth-child(2) td:nth-child(6) {
      background-color: #FFEDD8;
    }

    /* Header column - white smoke */
    table.addons tr th:first-child {
    background-color: #eff3f5;
    }
    
    /* Not applicable - light grey */
    table.addons tr:nth-child(3) td:nth-child(2), 
    table.addons tr:nth-child(4) td:nth-child(2) {
      background-color: #dee2e6;
    }
  

    /* Boilerplates */
   
    /* Header row - gray */
    table.boilerplates thead tr:first-child th {
      background-color: #ced4da !important;
    }

    /* Not allowed - red */
    table.boilerplates tr:nth-child(1), 
    table.boilerplates tr:nth-child(2), 
    table.boilerplates tr:nth-child(3) {
      background-color: #F9DEDE;
    }

    /* Allowed - green */
    table.boilerplates tr:nth-child(2) td:nth-child(2), 
    table.boilerplates tr:nth-child(3) td:nth-child(6),
    table.boilerplates tr:nth-child(4), tr:nth-child(5) {
      background-color: #E2E9C7;
    }

    /* Caution - yellow */
    table.boilerplates tr:nth-child(1) td:nth-child(6), 
    table.boilerplates tr:nth-child(2) td:nth-child(6){
      background-color: #FFEDD8;
    }

    /* Header column - white smoke */
    table.boilerplates tr th:first-child {
      background-color: #eff3f5;
    }
    
    /* Not applicable - light grey */
    table.boilerplates tr:nth-child(3) td:nth-child(2), 
    table.boilerplates tr:nth-child(4) td:nth-child(2) {
      background-color: #dee2e6;
    }


    /* Applications */

    /* Header row - gray */
    table.applications thead tr:first-child th {
      background-color: #ced4da !important;
    }

    /* Not allowed - red */
    table.applications tr:nth-child(1), 
    table.applications tr:nth-child(2),
    table.applications tr:nth-child(3) {
      background-color: #F9DEDE;
    }

    /* Allowed - light green */
    table.applications tr:nth-child(2) td:nth-child(2), 
    table.applications tr:nth-child(3) td:nth-child(3), 
    table.applications tr:nth-child(4) {
      background: #E2E9C7;
    }
    
     /* Header column - white smoke */
    table.applications tr th:first-child {
      background-color: #eff3f5;
    }
    
    /* Not applicable - light grey */
    table.applications tr:nth-child(3) td:nth-child(2) {
      background-color: #dee2e6;
    }

  </style>



Control panel permissions reference
===================================

The following table shows the different permission options for the different
types of users with respect to addons, boilerplates and applications.


Addons
------

.. list-table::
  :widths: 20 30 20 20 20 25 30
  :header-rows: 1
  :stub-columns: 1
  :class: addons

  * - User level
    - Create new addon
    - Manage addon settings
    - Manage addon collaborators
    - Upload new addon version
    - Install/ upgrade to a project [#f1]_ 
    - Manage settings on a project [#f1]_ 

  * - Anyone
    - |KHgr|
    - |KHgr|
    - |KHgr|
    - |KHgr|
    - Only for public addons
    - |check| Only for already installed addons

  * - Organisation collaborator
    - |check| Added as collaborator with "Can update"
    - |KHgr|
    - |KHgr|
    - |KHgr|
    - Only for public addons
    - |check| Only for already installed addons

  * - Addon collaborator
    - n/a
    - |KHgr|
    - |KHgr|
    - |KHgr|
    - |check|
    - |check|

  * - Addon collaborator with "Can update"
    - n/a
    - |check|
    - |check|
    - |check|
    - |check|
    - |check|

  * - Organisation owner/admin
    - |check|
    - |check|
    - |check|
    - |check|
    - |check|
    - |check|


Boilerplates
------------

.. list-table::
  :widths: 30 20 20 20 20 25
  :header-rows: 1
  :stub-columns: 1
  :class: boilerplates

  * - User level
    - Create new boilerplate
    - Manage boilerplate settings
    - Manage boilerplate collaborators
    - Upload new boilerplate version
    - Create a project with boilerplate

  * - Anyone
    - |KHgr|
    - |KHgr|
    - |KHgr|
    - |KHgr|
    - Only for public boilerplates

  * - Organisation collaborator
    - |check| Added as collaborator with "Can update"
    - |KHgr|
    - |KHgr|
    - |KHgr|
    - Only for public boilerplates

  * - Boilerplate collaborator
    - n/a
    - |KHgr|
    - |KHgr|
    - |KHgr|
    - |check|

  * - Boilerplate collaborator with "Can update"
    - n/a
    - |check|
    - |check|
    - |check|
    - |check|

  * - Organisation owner/admin
    - |check|
    - |check|
    - |check|
    - |check|
    - |check|


Applications
------------

.. list-table:: 
  :class: applications
  :widths: 20 20 20 20
  :header-rows: 1
  :stub-columns: 1

  * - User level
    - Create new application
    - Manage application settings
    - Manage collaborators

  * - Anyone
    - |KHgr|
    - |KHgr|
    - |KHgr|

  * - Organisation collaborator
    - |check| Added as collaborator
    - |KHgr|
    - |KHgr|

  * - Application collaborator 
    - n/a
    - |check|
    - |KHgr|
    
  * - Organisation owner/admin
    - |check|
    - |check|
    - |check|


.. [#f1] Access to a project is a prerequisite for this action.


# -*- coding: utf-8 -*-
@swisslux @setup @project

Feature: Cleanup project from example data

  @project_archive_default_data
  Scenario: Archive default data of project_data.xml
    Given I find a "project.project" with oid: project.project_project_data
    And having:
      | name   | value |
      | active | False |
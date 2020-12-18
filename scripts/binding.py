from cf_common import get_space_guid, cf_client_initialise, get_guid_within_space


def create_service_binding(app, app_guid, client, instance_guid):
    try:
        client.v2.service_bindings.create(
            app_guid=app_guid, instance_guid=instance_guid
        )
        print(f"Service binding created for {app_guid}")
    except Exception as e:
        print(f"Failed to create service binding for {app}: {e}")
        exit(1)


def binding_handler(app, instance, organisation, organisation_space):
    client = cf_client_initialise()
    space_guid = get_space_guid(
        client=client, organisation=organisation, organisation_space=organisation_space
    )
    app_guid = get_guid_within_space(
        client_search=client.v2.apps, identifier=app, space_guid=space_guid
    )
    instance_guid = get_guid_within_space(
        client_search=client.v2.service_instances,
        identifier=instance,
        space_guid=space_guid,
    )
    create_service_binding(
        app=app, app_guid=app_guid, client=client, instance_guid=instance_guid
    )

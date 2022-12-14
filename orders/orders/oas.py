from urllib import response
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import Schema,fields,validate
from oas_helpers import make_response,make_request_body,make_parameter


specification = APISpec(
    title='Orders Api',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[MarshmallowPlugin()],
    **{'info': {'description':'API that allows you to manage orders for CoffeeMesh'}},
      
)
class OrderItemSchema(Schema):
    product = fields.String(required=True)
    size = fields.String(
        required=True,validate=validate.OneOf(['small','medium','big'])
    )
    quantity = fields.Integer(
        default=1,validate=validate.Range(1,min_inclusive=True)
    )


class CreateOrderSchema(Schema):
    order = fields.List(fields.Nested(OrderItemSchema),required=True)

class GetOrderSchema(Schema):
    id = fields.UUID(required=True)
    created = fields.Integer(required=True)
    status = fields.String(
      required=True, validate=validate.OneOf(['active', 'cancelled', 'completed'])
    )
    order = fields.List(fields.Nested(OrderItemSchema), required=True)

specification.components.schema('GetOrderSchema',schema=GetOrderSchema)
specification.components.schema('CreateOrderSchema', schema=GetOrderSchema)



specification.path(
    path='/orders',
    operations={
        'get':{
            'description':(
                'A list of orders made by the customer sorted by date.Allows'
                'to filter orders by range of dates.\n'
            ),
            'responses':make_response(
                {'type':'object','properties':{'data': {'type':'array','items':{'%$ref': '#/components/schemas/GetOrderSchema'}}}},
                description='A JSON array of orders'
            )
        },
        'post':{
            'summary':'Create an Order',
            'requestBody':make_request_body('CreateOrderSchema'),
            'responses':make_response(
                'GetOrderSchema',status_code='201',
                description='A JSON representation of the created order'
            )
        }
    }
)


specification.path(
    path='/orders/{order_id}',
    parameters=[make_parameter(in_='path',name='order_id',schema={'type':'string'})],
    operations={
        'get':{
            'summary':'Returns the details of a specific order',
            'responses':make_response(
                'GetOrderSchema',description='A JSON representation of an order'
            )
        },
        'put':{
            'description':'Replaces an existing order',
            'requestBody':make_request_body('CreateOrderSchema'),
            'responses':make_response(
                'GetOrderSchema',description='A JSON representation of an order'
            )
        },
        'delete':{
            'description':'Deletes an existing order',

            'responses':{'204':{'description': 'The resource was deleted successfully'}}
        }
    }
)

print(specification.to_yaml())
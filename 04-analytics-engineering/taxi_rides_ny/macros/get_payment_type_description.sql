{#
    This macro returns the description of the payment_type.
    Assumes payment_type is a string that represents an integer.
#}

{% macro get_payment_type_description(payment_type) -%}
    case {{ payment_type }}
        when '1.0' then 'Credit card'
        when '1' then 'Credit card'
        when '2.0' then 'Cash'
        when '2' then 'Cash'
        when '3.0' then 'No charge'
        when '3' then 'No charge'
        when '4.0' then 'Dispute'
        when '4' then 'Dispute'
        when '5.0' then 'Unknown'
        when '5' then 'Unknown'
        when '6.0' then 'Voided trip'
        when '6' then 'Voided trip'
        else 'EMPTY'
    end
{%- endmacro %}

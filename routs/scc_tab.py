from flask import Blueprint, render_template, request, make_response
from database import query_database
import pandas as pd
import io

scc_tab_bp = Blueprint('scc_tab', __name__)

views = [
    '3way_trading_servicos_administra_ltda',
    'acai_kingdom_llc',
    'anjun',
    'apg_global',
    'arc_storck_florida_lcc',
    'br1express',
    'bringer_air_cargo',
    'bringer_corporation',
    'cainiao_br_gestao_logistica_ltda',
    'ch_import_conseil',
    'cne',
    'cosco_shipping_eglobal',
    'cross_border_hub',
    'ctc_logistica',
    'direct_link',
    'eagle_rock_log',
    'ecexpress',
    'expobox',
    'fashion_choice',
    'genie_shipping',
    'globetrans',
    'go_box_usa',
    'hangzhou_cainiao_suppy_chain_manag_co_lt',
    'home_delivery_br',
    'hub_america_logistica',
    'in_glow',
    'jet_international_ltda',
    'levelog_logistica',
    'lion_ecommerce',
    'mailamericas',
    'mercury_shine',
    'nkc_assessoria_e_logistica_eireli',
    'noss_servicos_em_logistica',
    'pfl',
    'royalway',
    'shps_tecnologia_e_servicos_ltda',
    'sinerlog_brasil_ltda',
    'sinerlogusa_packet',
    'sky_postal',
    'smart_data_trading_e_commerce_com_de_pr',
    'sunlog',
    'transamerica_usa',
    'vegway_import_e_distrib_de_alim_vegetari',
    'we_work_express',
    'wise_international',
    'wprime',
    'yide'
]


from database import query_database, get_armazem_summary

@scc_tab_bp.route('/SCC_TAB', methods=['GET', 'POST'])
def SCC():
    results = []

    # Consulta resumo da tabela armazem
    df_armazem = get_armazem_summary()
    if not df_armazem.empty:
        result = df_armazem.to_dict(orient='records')
        for r in result:
            r['view_name'] = r.pop('cliente')  # compatível com o HTML
            r['total_objetos'] = "{:,.0f}".format(r['total_objetos']).replace(",", ".")
        results = result

    # Se for POST, continua com a lógica atual
    if request.method == 'POST':
        if 'clear' in request.form:
            results = []
        else:
            view_name = request.form['view_name']
            if view_name != 'shp':
                df = query_database(view_name)
                if not df.empty:
                    result = df.to_dict(orient='records')
                    for r in result:
                        r['view_name'] = view_name
                        if "total_objetos" in r:
                            r["total_objetos"] = "{:,.0f}".format(r["total_objetos"]).replace(",", ".")
                    # Geração do CSV
                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False)
                    csv_bytes = io.BytesIO(csv_buffer.getvalue().encode('utf-8-sig'))
                    response = make_response(csv_bytes.getvalue())
                    response.headers["Content-Disposition"] = f"attachment; filename={view_name}.csv"
                    response.headers["Content-type"] = "text/csv; charset=utf-8"
                    return response
                else:
                    result = [{"view_name": view_name, "total_objetos": "0"}]
            if 'results' not in request.form:
                results = result
            else:
                results = eval(request.form['results']) + result
            results = results[-10:]

    return render_template('SCC_TAB.html', result=results, views=views)
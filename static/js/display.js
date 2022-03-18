function calc_points_left(){
    let points_left = document.querySelector(".points_left")
    let roster_cost = document.querySelector(".roster_cost").getAttribute("value")
    let roster_max_cost = document.querySelector(".roster_max_cost").getAttribute("value")
    points_left.innerText = `Points left: ${roster_max_cost - roster_cost}`
}

function calc_detachment_restrictions() {
    const classes_data = [
        [".result_hq", ".hq_restr"],
        [".result_troops", ".troops_restr"],
        [".result_elites", ".elites_restr"],
        [".result_f_attack", ".f_attack_restr"],
        [".result_flyers", ".flyers_restr"],
        [".result_h_support", ".h_support_restr"],
        [".result_l_o_w", ".l_o_w_restr"]
    ]
    for (let cl_data of classes_data) {
        let result_el = document.querySelector(cl_data[0])
        let all_restr_els = document.querySelectorAll(cl_data[1])

        let min = 0
        let max = 0
        for (let restr_el of all_restr_els) {
            let el_txt = restr_el.textContent

            let splitted_txt = el_txt.split("-")

            min += parseInt(splitted_txt[0])
            max += parseInt(splitted_txt[1])

        result_el.textContent = `${min}-${max}`
        }
    }
}

function calc_unit_cost(unit_el){
    let result_cost = 0
    let target_el = unit_el.querySelector(".unit_total_cost")
    let all_model_els = unit_el.querySelectorAll(".model_element")
    let all_weapon_els = unit_el.querySelectorAll(".w_element")
    let all_ability_els = unit_el.querySelectorAll(".ability_element")
    let all_wargear_els = unit_el.querySelectorAll(".wargear_element")

    for (let model of all_model_els) {
        let price = parseInt(model.querySelector(".m_price").textContent)
        let count = parseInt(model.querySelector(".m_count").textContent)
        result_cost += price * count
    }
    for (let weap of all_weapon_els) {
        let price = parseInt(weap.querySelector(".w_price").textContent)
        let count = parseInt(weap.querySelector(".w_count").textContent)
        result_cost += price * count
    }
    for (let abil of all_ability_els) {
        let price = abil.querySelector(".a_price")
        if (price != null) {
            console.log(price.textContent)
            result_cost += parseInt(price.textContent)
        }
    }
    for (let warg of all_wargear_els) {
        let price = warg.querySelector(".war_price")
        if (price != null) {
            result_cost += parseInt(price.textContent)
        }
    }
    target_el.textContent = result_cost
}

window.onload = function(){
    calc_points_left()
    calc_detachment_restrictions()

    for (let unit_el of document.querySelectorAll(".unit_element")) {
        calc_unit_cost(unit_el)
    }
}
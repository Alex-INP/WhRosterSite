function calc_points_left(){
    let points_left = document.querySelector(".points_left")
    let roster_cost = parseInt(document.querySelector(".roster_points").textContent)
    let roster_max_cost = document.querySelector(".roster_max_cost").getAttribute("value")
    let result = roster_max_cost - roster_cost
    if (result < 0) {
        points_left.classList.add("text-danger")
    } else {
        points_left.classList.add("model_cost")
    }
    points_left.innerText = `Points left: ${result}`
}

function reset_user_detachment_count(target) {
    const sources = {
        "hq": [".all_hq_units", ".roster_det_hq", ".result_hq"],
        "troops": [".all_troops_units", ".roster_det_troops", ".result_troops"],
        "elites": [".all_elites_units", ".roster_det_elites", ".result_elites"],
        "f_attack": [".all_f_attack_units", ".roster_det_f_attack", ".result_f_attack"],
        "flyers": [".all_flyers_units", ".roster_det_flyers", ".result_flyers"],
        "h_support": [".all_h_support_units", ".roster_det_h_support", ".result_h_support"],
        "l_o_w": [".all_l_o_w_units", ".roster_det_l_o_w", ".result_l_o_w"]
    }
    let settings = sources[target]
    let units_count = document.querySelector(settings[0]).querySelectorAll(".unit_entity_el").length
    let target_result_el = document.querySelector(settings[1])
    let restrictions = document.querySelector(settings[2]).textContent.split("-")

    let min = parseInt(restrictions[0])
    let max = parseInt(restrictions[1])
    if ( target_result_el != null){
        target_result_el.textContent = units_count
        if (min <= units_count && units_count <= max){
            target_result_el.classList.add("text-primary")
        } else {
            target_result_el.classList.add("text-danger", "fw-bold")
        }
    }
}

function calc_detachment_restrictions() {
    const classes_data = [
        [".result_hq", ".hq_restr", "hq"],
        [".result_troops", ".troops_restr", "troops"],
        [".result_elites", ".elites_restr", "elites"],
        [".result_f_attack", ".f_attack_restr", "f_attack"],
        [".result_flyers", ".flyers_restr", "flyers"],
        [".result_h_support", ".h_support_restr", "h_support"],
        [".result_l_o_w", ".l_o_w_restr", "l_o_w"]
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
    reset_user_detachment_count(cl_data[2])
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

function count_roster_total_points() {
    let result = 0
    let all_units_els = document.querySelectorAll(".unit_element")
    for( let unit of all_units_els) {
        let unit_cost = unit.querySelector(".unit_total_cost").textContent
        result += parseInt(unit_cost)
    }
    document.querySelector(".roster_points").textContent = result
}


window.onload = function(){
    calc_detachment_restrictions()
    for (let unit_el of document.querySelectorAll(".unit_element")) {
        calc_unit_cost(unit_el)
    }
    count_roster_total_points()
    calc_points_left()
}

const funfun = function(){console.log("meme")}
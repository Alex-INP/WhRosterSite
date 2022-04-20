"use strict";

function total_recalc(){
    for (let unit_el of document.querySelectorAll(".unit_element")) {
        calc_unit_cost(unit_el)
    }
    count_roster_total_points()
    calc_points_left()
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
        if (price != null && abil.querySelector("div[bought='true']") != null) {
            result_cost += parseInt(price.textContent)
        }
    }
    for (let warg of all_wargear_els) {
        let price = warg.querySelector(".war_price")

        if (price != null && warg.querySelector("div[bought='true']") != null) {
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

const delete_detach_func = function(){
        let detachment_row_el = $(this).parent().parent()
        detachments.delete_detach_id(detachment_row_el.attr("detach_id"))
        detachment_row_el.remove()
        calc_detachment_restrictions()
    }

let all_detachments_el = $(".all_detachments_segment")
all_detachments_el.hide()

$(".all_detach_close_btn").click(function(){
    all_detachments_el.hide()
})
$(".add_new_detachment_btn").click(function(){
    all_detachments_el.show()
})


class UserDetachments{
    constructor(){
        this.detachments_id = []
    }

    collect_detachments(){
        for(let elem of $(".detachment_data")){
            this.detachments_id.push($(elem).attr("detach_id"))
        }
    }

    add_detach_id(id){
        this.detachments_id.push(id)
    }

    delete_detach_id(id){
        this.detachments_id.splice(this.detachments_id.indexOf(id), 1)
    }
}

const detachments = new UserDetachments()
detachments.collect_detachments()

$(".add_detachment_btn").click(function(){
    let detachment_row_el = $(this).parent().parent()
    detachments.add_detach_id(detachment_row_el.attr("detach_id"))
    $(".detachment_blank_row").before(`
        <tr class="detachment_data" detach_id="${detachment_row_el.attr('detach_id')}">
            <td>${$(detachment_row_el).find(".detach_name_all").text()}</td>
            <td class="text-center">${$(detachment_row_el).find(".detach_command_cost_all").text()}</td>
            <td>${$(detachment_row_el).find(".detach_restrictions_all").text()}</td>
            <td>${$(detachment_row_el).find(".detach_command_benefits_all").text()}</td>
            <td>${$(detachment_row_el).find(".detach_transport_restriction_all").text()}</td>
            <td class="text-center hq_restr">${$(detachment_row_el).find(".hq_restr_all").text()}</td>
            <td class="text-center troops_restr">${$(detachment_row_el).find(".troops_restr_all").text()}</td>
            <td class="text-center elites_restr">${$(detachment_row_el).find(".elites_restr_all").text()}</td>
            <td class="text-center f_attack_restr">${$(detachment_row_el).find(".f_attack_restr_all").text()}</td>
            <td class="text-center flyers_restr">${$(detachment_row_el).find(".flyers_restr_all").text()}</td>
            <td class="text-center h_support_restr">${$(detachment_row_el).find(".h_support_restr_all").text()}</td>
            <td class="text-center l_o_w_restr">${$(detachment_row_el).find(".l_o_w_restr_all").text()}</td>
            <td class="text-center"><button class="delete_detachment_btn btn btn-danger">Delete</button></td>
        </tr>`
        )
    let delete_detach_btn = $(".delete_detachment_btn")
    delete_detach_btn.unbind()
    delete_detach_btn.click(delete_detach_func)
    calc_detachment_restrictions()
    }
)

$(".delete_detachment_btn").click(delete_detach_func)

const factions_id = []
for(let el of $(".faction_id").text()){
    factions_id.push(el)
}

//---------------------------------------------

//class Unit{
//    constructor(id){
//    //position_number
//    this.unit_pk = id
//    this.models = [{"model_pk": 1, "model_count": 1}]
//    this.weapon = [{"weapon_pk": 1, "weapon_count": 1}]
//    this.abilities = [{"ability_pk": 1, "bought": true}]
//    this.other_wargear = [{"wargear_pk": 1, "bought": true}]
//    }
//}

class Unit{
    constructor(id){
    this.unit_pk = id
    this.models = []
    this.weapon = []
    this.abilities = []
    this.other_wargear = []
    }
}

let last_observed = null
$(".observe_unit").click(function(){
    let target_id = $(this).attr("observe_id")
    let result = $(".codex_unit_template")
    for(let res of result){
            if($(res).attr("id") === target_id){
                $(res).show()
                if(last_observed === null){
                    last_observed = $(res)
                } else {
                    last_observed.hide()
                    last_observed = $(res)
                }
                break
            }
        }
    }
)

let unit_choose_hide = true
$(".new_roster_unit_btn").click(function(){
        let unit_choose_el = $(".unit_choose_wrapper")
        let docked_menu = $(".dock_side_unit_menu")
        if(unit_choose_hide == true){
            unit_choose_el.show()
            unit_choose_hide = false
        } else {
            unit_choose_el.hide()
            unit_choose_hide = true
        }
    }
)
//for(let el of factions_id){
//        $.ajax({
//        url: `http://127.0.0.1:8000/builder/manage_roster_ajax/${el}`,
//        headers: {
//            "ajax_request": "true"
//        },
//        type: "GET",
//        success: function(data){
//            console.log(data);
//        }
//    })
//}

window.onscroll = function(){checkSideMenu()}

const menu = $(".side_menu")
const position = $(".new_roster_unit_btn").offset()["top"]
function checkSideMenu(){
  if (window.pageYOffset > position) {
    menu.addClass("dock_side_unit_menu")
    menu.removeClass("side_menu")
  } else {
    menu.removeClass("dock_side_unit_menu")
    menu.addClass("side_menu")
  }
}

const model_btn_plus_els = $(".model_btn_plus")
const model_btn_minus_els = $(".model_btn_minus")
model_btn_plus_els.click(change_model_count_value)
model_btn_minus_els.click(change_model_count_value)

function change_model_count_value(){
    let model_row_el = $(this).parents(".model_element")

    let current_model_count_el = model_row_el.find("span.count_stl.m_count")

    let current_model_count = parseInt(current_model_count_el.text())
    let current_model_max_count = parseInt(model_row_el.find("span.max_restriction").text())
    if($(this).html() == "+") {
        if(current_model_count < current_model_max_count){
            current_model_count_el.html(current_model_count + 1)
            total_recalc()
        }
    } else if($(this).html() == "-") {
        if(current_model_count != 0) {
            current_model_count_el.html(current_model_count - 1)
            total_recalc()
        }
    }
}

const weapon_btn_plus_els = $(".weapon_btn_plus")
const weapon_btn_minus_els = $(".weapon_btn_minus")
weapon_btn_plus_els.click(change_weapon_count_value)
weapon_btn_minus_els.click(change_weapon_count_value)

function change_weapon_count_value(){
    let weapon_row_el = $(this).parents(".weapon_row")
    let current_weapon_count_el = weapon_row_el.find("div.w_count")
    let current_weapon_count = parseInt(current_weapon_count_el.text())

    if($(this).html() == "+") {
        current_weapon_count_el.html(current_weapon_count + 1)
        total_recalc()

    } else if($(this).html() == "-") {
        if(current_weapon_count != 0) {
            current_weapon_count_el.html(current_weapon_count - 1)
            total_recalc()
        }
    }
}

const ability_btn_plus_els = $(".ability_btn_plus")
ability_btn_plus_els.click(buy_ability)

function buy_ability(){
    let ability_row_el = $(this).parents(".ability_element")
    let ability_bought_el = ability_row_el.find("[bought]")
}


const wargear_btn_plus_els = $(".wargear_btn_plus")
wargear_btn_plus_els.click(buy_wargear)

function buy_wargear(){
    let wargear_row_el = $(this).parents(".wargear_element")
    let wargear_bought_el = wargear_row_el.find("[bought]")
    if(wargear_bought_el.attr("bought") == "true") {
        wargear_bought_el.attr("bought", "false")

        wargear_bought_el.removeClass("border-success")
        wargear_bought_el.addClass("border-danger")

        total_recalc()
    } else {
        wargear_bought_el.attr("bought", "true")

        wargear_bought_el.removeClass("border-danger")
        wargear_bought_el.addClass("border-success")

        total_recalc()
    }
}

const delete_unit_btn = $(".delete_unit_btn")
delete_unit_btn.click(function(){
    let delete_section_el = $(this).parent()
    let unit_element_id = `[id='${$(this).attr("related_unit_id")}']`
    let unit_to_delete_el = $("" + unit_element_id)
    delete_section_el.remove()
    unit_to_delete_el.remove()
    }
)

for(let el of $(".unit_element")){
    change_unit_signature(el, "up")
}
function change_unit_signature(jquery_unit_el, command){
    let target = $(jquery_unit_el)
    let target_id = target.attr("id")
    let target_position = target.attr("position")
    let target_name = target.attr("name")
    let target_delete_button = $("" + `[related_unit_id="${target_id}"]`)
    let target_anchors = $(`[href='#${target_id}']`)
    let new_position
    if(command == "up") {
        new_position = parseInt(target_position) + 1
    } else if(command == "down") {
        new_position = parseInt(target_position) - 1
    }
    let new_id = `${new_position}/${target_name}`

    target_delete_button.attr("related_unit_id", new_id)
    target.attr("id", new_id)
    target.attr("position", new_position)

    let double = true
    let anchors_len = target_anchors.length
    for(let anchor of $(target_anchors)) {
        if(double == true && anchors_len != 2){
            double = false
            continue
        }
        $(anchor).attr("href", `#${new_id}`)
        double = true
    }
}

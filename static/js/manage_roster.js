"use strict";

$(".save_response_element").hide()

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
    let result = $(".unit_element_template")
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
delete_unit_btn.click(delete_unit_event)

function delete_unit_event(){
    let delete_section_el = $(this).parent()
    let unit_element_id = `[id='${$(this).attr("related_unit_id")}']`
    let unit_to_delete_el = $(unit_element_id)
    let menu_els = $(`[href='#${$(this).attr("related_unit_id")}']`)

    let unit_element_position = unit_to_delete_el.attr("position")
    reposition_upon_delete(unit_element_position)

    delete_section_el.remove()
    unit_to_delete_el.remove()
    menu_els.remove()
    total_recalc()
}

function reposition_upon_delete(delete_position){
    let all_unit_els = $(".unit_element")
    for(let unit_el of all_unit_els) {
        if($(unit_el).attr("position") > delete_position){
            change_unit_signature(unit_el, "up")
        }
    }
}

//for(let el of $(".unit_element")){
//    change_unit_signature(el, "up")
//}
function change_unit_signature(jquery_unit_el, command){
    let target = $(jquery_unit_el)
    let target_id = target.attr("id")
    let target_position = target.attr("position")
    let target_name = target.attr("name").split(" ").join("")
    let target_delete_button = $("" + `[related_unit_id="${target_id}"]`)
    let target_anchors = $(`[href='#${target_id}']`)
    let new_position
    if(command == "up") {
        new_position = parseInt(target_position) - 1
    } else if(command == "down") {
        new_position = parseInt(target_position) + 1
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


$(".add_new_unit_btn").click(function(){
        let unit_template_id = $(this).parent().find("a").attr("observe_id")
        let target_template = $(`[id='${unit_template_id}']`)

        let last_unit_element = $(".unit_element").last()

        let last_position_index = parseInt(last_unit_element.attr("position"))

        let new_position
        let new_id
        let result_unit_el
        if (last_unit_element.length != 0) {
            new_position = last_position_index + 1
            new_id =`${new_position}/${target_template.attr("name").split(" ").join("")}`
            result_unit_el = target_template.clone()
                .attr("id", new_id)
                .attr("position", new_position)
                .removeClass("unit_element_template")
                .addClass("unit_element")

            last_unit_element.after(result_unit_el)
            last_unit_element.after(create_unit_header(new_id))
        } else {
            new_position = 1
            new_id =`${new_position}/${target_template.attr("name").split(" ").join("")}`
            result_unit_el = target_template.clone()
                    .attr("id", new_id)
                    .attr("position", new_position)
                    .removeClass("unit_element_template")
                    .addClass("unit_element")

            let units_container_el = $(".added_units_container")
            units_container_el.html(result_unit_el)
            units_container_el.prepend(create_unit_header(new_id))
        }

        let role_name = $(target_template).find(".battlefield_role").html().toLowerCase()
        let unit_name = target_template.attr("name")

        add_el_top_menu(new_id, unit_name, role_name)
        add_el_docked_menu(new_id, unit_name, role_name)
        rebind_unit_eventHandlers()
    }
)

function create_unit_header(unit_id){
    let header_html = `
        <div class="container border border-2 border-dark d-flex justify-content-between mt-3 model_bgr">
            <div>
                <button class="up_unit_btn border border-2 border-dark btn btn-primary m-2">Up</button>
                <button class="down_unit_btn border border-2 border-dark btn btn-primary m-2">Down</button>
            </div>
            <button class="delete_unit_btn border border-2 border-dark btn btn-danger m-2" related_unit_id="${unit_id}">Delete Unit</button>
        </div>`
    return header_html
}

function add_el_top_menu(unit_id, unit_name, unit_role){
    let entry_html = `<a href=#${unit_id} class="bg-secondary text-light p-2 border border-dark link_underline unit_entity_el">${unit_name}</a>`
    let all_menu_segments = $(".top_menu_segment")
    for(let element of all_menu_segments){
        if($(element).children("h4").html().toLowerCase() == unit_role){
            $(element).find("div").first().append(entry_html)
        }
    }
}

function add_el_docked_menu(unit_id, unit_name, unit_role){
    let entry_html = `<a href=#${unit_id} class="side_menu_unit bg-secondary text-light p-2 border border-dark link_underline unit_entity_el">${unit_name}</a>`
    let all_menu_segments = $(".side_menu_segment")
    for(let element of all_menu_segments){
        if($(element).children(".side_menu_detachment_header").html().toLowerCase() == unit_role){
            $(element).children().eq(1).append(entry_html)
        }
    }
}

function rebind_unit_eventHandlers(){
    let delete_unit_btn = $(".delete_unit_btn")
    delete_unit_btn.unbind()
    delete_unit_btn.click(delete_unit_event)

    let wargear_btn_plus_els = $(".wargear_btn_plus")
    if(wargear_btn_plus_els.length != 0){
        wargear_btn_plus_els.unbind()
        wargear_btn_plus_els.click(buy_wargear)
    }

    let ability_btn_plus_els = $(".ability_btn_plus")
    if(ability_btn_plus_els.length != 0){
        ability_btn_plus_els.unbind()
        ability_btn_plus_els.click(buy_ability)
    }

    let weapon_btn_plus_els = $(".weapon_btn_plus")
    if(weapon_btn_plus_els.length != 0){
        weapon_btn_plus_els.unbind()
        weapon_btn_plus_els.click(change_weapon_count_value)
    }

    let weapon_btn_minus_els = $(".weapon_btn_minus")
    if(weapon_btn_minus_els.length != 0){
        weapon_btn_minus_els.unbind()
        weapon_btn_minus_els.click(change_weapon_count_value)
    }

    let model_btn_plus_els = $(".model_btn_plus")
    if(model_btn_plus_els.length != 0){
        model_btn_plus_els.unbind()
        model_btn_plus_els.click(change_model_count_value)
    }

    let model_btn_minus_els = $(".model_btn_minus")
    if(model_btn_minus_els.length != 0){
        model_btn_minus_els.unbind()
        model_btn_minus_els.click(change_model_count_value)
    }

    const up_down_unit_btn_els = $(".up_unit_btn, .down_unit_btn")
    up_down_unit_btn_els.unbind()
    up_down_unit_btn_els.click(element_reposition)
}

const up_down_unit_btn_els = $(".up_unit_btn, .down_unit_btn")
up_down_unit_btn_els.click(element_reposition)

function element_reposition(){
    let target_unit_header = $(this).parents(".container")
    let target_unit_id = target_unit_header.find("button.delete_unit_btn").attr("related_unit_id")
    let target_unit_el = $(`[id='${target_unit_id}']`)

    let directive
    let other_unit_position
    if($(this).text().toLowerCase() == "up"){
        other_unit_position = parseInt(target_unit_el.attr("position")) - 1
        directive = "up"
    } else {
        other_unit_position = parseInt(target_unit_el.attr("position")) + 1
        directive = "down"
    }

    let other_unit_el = $(`[position='${other_unit_position}']`)
    let other_unit_id = other_unit_el.attr("id")
    let other_unit_header_el = $(`[related_unit_id='${other_unit_id}']`).parent()
    if(other_unit_el.length == 0){
        return
    }

    if(directive == "up"){
        other_unit_header_el.before(target_unit_el)
        target_unit_el.before(target_unit_header)

        change_unit_signature(target_unit_el, "up")
        change_unit_signature(other_unit_el, "down")
    } else {
        target_unit_header.before(other_unit_el)
        other_unit_el.before(other_unit_header_el)

        change_unit_signature(target_unit_el, "down")
        change_unit_signature(other_unit_el, "up")
    }

    console.log("trig")
}

$(".save_roster_btn").click(function(){
    let roster_id = $(".roster_id").text()
    let data = collect_send_data()
    data.roster_id = roster_id

    fetch(`http://127.0.0.1:8000/builder/manage_roster/${roster_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8",
            "X-CSRFToken": get_csrf()
        },
        body: JSON.stringify(data),
        credentials: 'same-origin'
        }).then(
            function(data){
                let response_el = $(".save_response_element")
                if(data.status == 200){
                    response_el.show()
                } else if(data.status == 500){
                    response_el.find("h4").text("Saving error")
                    response_el.removeClass("bg-success")
                    response_el.addClass("bg-danger")
                    response_el.show()
                }

                setTimeout(function(){
                    $(".save_response_element").hide()
                }, 5000)
            }
        )
})


function get_csrf(){
    let cookies = document.cookie.split(";")
    for(let cookie of cookies){
        let cookie_data = cookie.split("=")
        if(cookie_data[0] == "csrftoken"){
            return cookie_data[1]
        }
    }
}

function collect_send_data(){
    let result = {
        roster_id: null,
        data: {
            detachment_data: [],
            main_data: []
        }
    }

    for(let detachment_el of $(".detachment_data")) {
        result.data.detachment_data.push($(detachment_el).attr("detach_id"))
    }

    for(let unit_el of $(".unit_element")) {
        unit_el = $(unit_el)
        let unit_data = {
            position_number: parseInt(unit_el.attr("position")),
            unit_pk: parseInt(unit_el.attr("fetch_id")),
            models: [],
            weapons: [],
            abilities: [],
            other_wargear:[]
        }

        let model_els = unit_el.find(".model_element")
        for(let model of model_els) {
            model = $(model)
            unit_data.models.push({
                model_pk: parseInt(model.attr("model_id")),
                model_count: parseInt(model.find(".m_count").text())
            })
        }

        let weapon_els = unit_el.find(".w_element")
        for(let weapon of weapon_els) {
            weapon = $(weapon)
            unit_data.weapons.push({
                weapon_pk: parseInt(weapon.attr("weapon_id")),
                weapon_count: parseInt(weapon.find(".w_count").text().trim())
            })
        }

        let abilities_els = unit_el.find(".ability_element")
        for(let ability of abilities_els) {
            ability = $(ability)
            let bought = ability.find("[bought]").attr("bought")
            if(bought == "undefined" || "true") {
                bought = true
            } else if(bought == "false"){
                bought = false
            }

            let abilities_data = {
                ability_pk: parseInt(ability.attr("ability_id")),
                bought: bought
            }

            unit_data.abilities.push(abilities_data)
//            if(Object.keys(abilities_data).length === 0){
//                unit_data.abilities.push(abilities_data)
//            }
        }

        let other_wargear_els = unit_el.find(".wargear_element")
        for(let wargear of other_wargear_els) {
            wargear = $(wargear)
            unit_data.other_wargear.push({
                wargear_pk: parseInt(wargear.attr("wargear_id")),
                wargear_count: (wargear.find("[bought]").attr("bought") == "true" ? 1 : 0)
            })
        }
        result.data.main_data.push(unit_data)
    }
    console.log(result)
    return result
}


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
        console.log(min)
        console.log("---")
        for (let restr_el of all_restr_els) {
            let el_txt = restr_el.textContent

            let splitted_txt = el_txt.split("-")

            min += parseInt(splitted_txt[0])
            max += parseInt(splitted_txt[1])

        result_el.textContent = `${min}-${max}`
        }

    }

}

window.onload = function(){
    calc_points_left()
    calc_detachment_restrictions()
}
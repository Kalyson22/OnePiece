const KEY_BD = '@OnePiece'

var listaArcos ={
    ultimoID:0,
    arcos:[]
}
var FILTRO = ''

function desenhar(){
    const tbody = document.getElementById('listaArcosBody')
    if(tbody){
        var data = listaArcos.arcos;
        if(FILTRO.trim()){
            const expReg = eval(`/${FILTRO.trim().replace(/[^\d\w]+/g,'.*')}/i`)
            data = data.filter( arco => {
                return expReg.test( arco.nome ) || expReg.test( arco.fone )
            } )
        }
        data = data
            .sort( (a, b) => {
                return a.nome < b.nome ? -1 : 1
            })
            .map( arco => {
                return `<tr>
                        <td>${arco.id}</td>
                        <td>${arco.nome}</td>
                        <td>${arco.fone}</td>
                        <td>
                            <button onclick='vizualizar("cadastro",false,${arco.id})'>Editar</button>
                            <button class='vermelho' onclick='perguntarSeDeleta(${arco.id})'>Deletar</button>
                        </td>
                    </tr>`
            } )
        tbody.innerHTML = data.join('')
    }
}

function inserir(nomeArco, episodios, ano, descricao){
    const id - listaArcos.ultimoID +1
    listaArcos.arcos.push({
        id, nomeArco, episodios, ano, descricao
    })
}
function Editar(id, nomeArco, episodios, ano, descricao){

}
function deletar(id){

}
function vizualizar(pagina){
    document.body.setAttribute('page', pagina);
    if(pagina=='cadastros'){
        document.getElementById('nomeArco').focus()
    }
}

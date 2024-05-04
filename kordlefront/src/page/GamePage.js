import AnswerBar from "../asset/component/AnswerBar";
import checkWord from "../asset/component/AnswerBar";
import Maker from "../asset/component/Maker";
import "../asset/component/background.css"
import {getTodayWord, getChangeNum, getValidation} from "../api/PostApi";
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { clearUserWord } from "../store/dataslice";

const buttonStyle={
    backgroundColor: '#4CAF50',
    border: 'none',
    color: 'white',
    padding: '10px 20px',
    textAlign: 'center',
    textDecoration: 'none',
    display: 'inline-block',
    fontSize: '16px',
    borderRadius: '5px',
    cursor: 'pointer',
    marginTop: '20px',
};

const hoverStyle = {
    backgroundColor: 'green',
};


function GamePage(){
    const [hover,setHover]=useState(false);
    const [count,setCount]=useState(1); //사용자 시도 횟수
    const [todayWord,setTodayWord]=useState([]);
    // const [isValid,setIsValid] = useState(false);

    const isdisabled=(count) >6 || count==-1 ? true : false; 
    var isValid;

    const dispatch=useDispatch();
    const data=useSelector((state)=>{
        return state.data;
      });

    console.log("재 랜더링")
    console.log(count)
    console.log(todayWord);

    function get_today_word(){
        getTodayWord().then((data)=>{
            setTodayWord(data);
        });  //
    }

    
    useEffect(() => {
        console.log("몇번 실행될까");
        get_today_word();
        // const intervalId = setInterval(get_today_word, 60 * 1000);
        // return () => clearInterval(intervalId); // 컴포넌트가 언마운트될 때 interval을 정리합니다.  // 상태가 변경될 때마다 실행됩니다.
      },[]);
    
    
    return(
        <div className="backGround">
            <div>
                <Maker></Maker>
            </div>
            <div>
                <AnswerBar id="1" count={count}></AnswerBar>
                <AnswerBar id="2" count={count}></AnswerBar>
                <AnswerBar id="3" count={count}></AnswerBar>
                <AnswerBar id="4" count={count}></AnswerBar>
                <AnswerBar id="5" count={count}></AnswerBar>
                <AnswerBar id="6" count={count}></AnswerBar>
            </div>
            <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center',}}>
                <button disabled={isdisabled} type="submit" style={hover ? { ...buttonStyle, ...hoverStyle } : buttonStyle} onMouseOver={() => setHover(true)} onMouseOut={() => setHover(false)} onClick={()=>{
                    var inputs = document.querySelectorAll('input[name^="input"]');
                    var elements=[];
                    var userWord=[];
                    var greenCount=0;

                    console.log(todayWord);
                    for(let i=(count-1)*6;i<(count-1)*6+6;i++){
                        userWord.push(inputs[i].value);
                        elements.push(inputs[i])
                        if(inputs[i].value==""){
                            alert("단어를 모두 입력해주세요")
                            return null;
                        }
                    }
                    const valid_data={"validWord": userWord};
                    getValidation(valid_data)
                    .then((data) => {
                        isValid = data;
                        if(isValid){
                            for(let i=0;i<6;i++){
                                console.log(userWord[i]==todayWord[i])
                                if(userWord[i]==todayWord[i]){
                                    elements[i].style.color = "white"
                                    elements[i].style.transition = "background-color 0.7s ease"
                                    elements[i].style.backgroundColor ='green';
                                    greenCount=greenCount+1;
                                }
                                else if(todayWord.includes(elements[i].value)){
                                    elements[i].style.color = "white"
                                    elements[i].style.transition = "background-color 0.7s ease"
                                    elements[i].style.backgroundColor = '#FFA500';
                                }
                                else{
                                    elements[i].style.color = "white"
                                    elements[i].style.transition = "background-color 0.7s ease"
                                    elements[i].style.backgroundColor = 'gray';
                                }
                            }
                            console.log(greenCount)
                            if(greenCount==6){
                                setCount(-1);
                            }
                            else{
                                setCount(count+1)
                                dispatch(clearUserWord());
                                console.log(count)
                            }
                        }
                        else{
                            alert("유효하지 않습니다.")
                            return null;
                        } // 비동기 작업이 완료된 후에 실행됩니다.
                    });

                    
                    // for(let i=0;i<6;i++){
                    //     console.log(userWord[i]==todayWord[i])
                    //     if(userWord[i]==todayWord[i]){
                    //         elements[i].style.color = "white"
                    //         elements[i].style.transition = "background-color 0.7s ease"
                    //         elements[i].style.backgroundColor ='green';
                    //         greenCount=greenCount+1;
                    //     }
                    //     else if(todayWord.includes(elements[i].value)){
                    //         elements[i].style.color = "white"
                    //         elements[i].style.transition = "background-color 0.7s ease"
                    //         elements[i].style.backgroundColor = '#FFA500';
                    //     }
                    //     else{
                    //         elements[i].style.color = "white"
                    //         elements[i].style.transition = "background-color 0.7s ease"
                    //         elements[i].style.backgroundColor = 'gray';
                    //     }
                    // }
                    // console.log(greenCount)
                    // if(greenCount==6){
                    //     setCount(-1);
                    // }
                    // else{
                    //     setCount(count+1)
                    //     console.log(count)
                    // }
                    
                }}>입력</button>
            </div>
        </div>
    );
}

export default GamePage